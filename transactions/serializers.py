from .models import Transaction
from rest_framework import serializers
from authentication.utils import field_error
from accounting.models import TransactionTypeBase
from django.db import transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'created_at', 'account']
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
        
        if transaction_type == TransactionTypeBase.TransactionTypes.OUTCOME and account.balance < amount:
            return field_error("account", "Insufficient funds")
        
        return attrs
    
        
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
        
        if account.balance < amount:
            return field_error("account", "Insufficient funds")
        
        return attrs
    
    def create(self, validated_data):
        amount = validated_data['amount']
        recipient = validated_data['recipient']
        account = validated_data['account']
        user = self.context.get('user')
        
        with transaction.atomic():
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
                "transaction_type": "Replenish",
                "account": transfer_from.account.account_type.name
            },
            "transfer_to": {
                "id": transfer_to.id,
                "transaction_type": "Replenish",
                "account": transfer_from.account.account_type.name
            }
        }

        