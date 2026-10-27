from .models import Transaction
from rest_framework import serializers
from authentication.utils import field_error
from accounting.models import TransactionTypeBase


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_type', 'created_at', 'account']
        read_only_fields = ['created_at']
        
        
    def validate(self, attrs):
        amount = attrs['amount']
        account = attrs['account']
        transaction_type = attrs['transaction_type']
        user = self.context.get('user')
        
        if not user.accounts.filter(pk=account).exists():
            return field_error("account", "Account not found")
        
        if transaction_type == TransactionTypeBase.TransactionTypes.OUTCOME and account.balance < amount:
            return field_error("account", "Insufficient funds")
        
            
        
        