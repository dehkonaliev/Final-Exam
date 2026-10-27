from .models import Transaction
from rest_framework import serializers
from authentication.utils import field_error
from accounting.models import TransactionTypeBase
from django.db import transaction
from django.db.models import F
from accounting.models import Account
import requests
import json
from decimal import Decimal, ROUND_HALF_UP

currencies = requests.get('https://cbu.uz/en/arkhiv-kursov-valyut/json/')
needed_currencies = {x['Ccy']:x['Rate'] for x in currencies.json() if x['Ccy'] in Account.CurrencyTypes.values}

def exchange_currency(amount, currency):
    if currency not in Account.CurrencyTypes.values:
        return field_error("currency", "Currency not found")
    if currency != 'UZS':
        return (amount/Decimal(needed_currencies[currency])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        return amount

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'created_at', 'transaction_type', 'account']
        read_only_fields = ['id', 'created_at']
        
    def validate(self, attrs):
        amount = attrs['amount']
        account = attrs['account']
        transaction_type = attrs['transaction_type']
        user = self.context.get('user')
        if not transaction_type:
            return field_error("transaction_type", "This field is required")
        if not user.accounts.filter(pk=account.id).exists():
            return field_error("account", "Account not found")
        
        if transaction_type.type == TransactionTypeBase.TransactionTypes.OUTCOME and account.balance < amount:
            return field_error("account", "Insufficient funds")
        
        return attrs
    
    def create(self, validated_data):
        transaction_type = validated_data.get('transaction_type')
        account = validated_data.get('account')
        amount = validated_data.get('amount')
        
        with transaction.atomic():
            account_obj = Account.objects.select_for_update().get(id=account.id)
            
            if transaction_type.type == TransactionTypeBase.TransactionTypes.OUTCOME:
                account_obj.balance = F('balance') - amount
            if transaction_type.type == TransactionTypeBase.TransactionTypes.INCOME:
                account_obj.balance = F('balance') + amount
            account_obj.save()
            
            return Transaction.objects.create(transaction_type=transaction_type, account=account, amount=amount)
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        account = instance.account
        if instance.transaction_type:
            representation['transaction_type'] = {
                "name": instance.transaction_type.name,
                "type": instance.transaction_type.type         
            }
            representation['account'] = {
                "name": account.account_type.name,
                "changed balance": exchange_currency(instance.changed_balance, account.currency),
                "currency": account.currency
            }
        return representation
            
        
    
        
class TransferToMeSerializer(serializers.ModelSerializer):
    recipient = serializers.IntegerField(required=True, write_only=True)
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'created_at', 'account', 'recipient']
        read_only_fields = ['id', 'created_at']
        
    def validate(self, attrs):
        amount = attrs['amount']
        account = attrs['account']
        recipient = attrs['recipient']
        user = self.context.get('user')
        
        if not user.accounts.filter(pk=account.id).exists():
            return field_error("account", "Account not found")
        
        if not user.accounts.filter(pk=recipient).exists():
            return field_error("recipient", "Recipient account not found")
        
        if account.id == recipient:
            return field_error("account", "Account and recipient cannot be the same")
        
        if account.balance < amount:
            return field_error("account", "Insufficient funds")
        
        return attrs
    
    def create(self, validated_data):
        amount = validated_data['amount']
        recipient = validated_data['recipient']
        account = validated_data['account']
        
        with transaction.atomic():
            sender_account = Account.objects.select_for_update().get(id=account.id)
            recipient_account = Account.objects.select_for_update().get(id=recipient)
            
            sender_account.balance = F('balance') - amount
            sender_account.save()
            
            recipient_account.balance = F('balance') + amount
            recipient_account.save()
            
            transfer_to = Transaction.objects.create(amount=amount, account_id=recipient, transaction_type_id=6)
            transfer_from = Transaction.objects.create(amount=amount, account=account, transaction_type_id=5)
        
        return {
            'transfer_to': transfer_to,
            "transfer_from": transfer_from
        }
        
    def to_representation(self, instance):
        transfer_from = instance['transfer_from']
        transfer_to = instance['transfer_to']
        return {
            "amount": transfer_from.amount,
            "created_at": transfer_from.created_at,
            "transfer_from": {
                "id": transfer_from.id,
                "transaction_type": "Transfer to me",
                "account": transfer_from.account.account_type.name,
                "balance": exchange_currency(transfer_from.changed_balance, transfer_from.account.currency)
                    
            },
            "transfer_to": {
                "id": transfer_to.id,
                "transaction_type": "Transfer from me",
                "account": transfer_from.account.account_type.name,
                "balance": exchange_currency(transfer_to.changed_balance, transfer_to.account.currency)
            }
        }

        