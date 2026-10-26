from rest_framework import serializers
from .models import TransactionTypeBase, TransactionTypePrivate, Transaction, AccountBase, Account
from authentication.utils import field_error

    

class AccountSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'currency', 'account_name']
        read_only_fields = ['id']

    def validate(self, attrs):
        name = attrs.get('account_name')
        user = self.context.get('user')
        
        account_obj = AccountBase.objects.filter(name=name).first()
        
        if account_obj and Account.objects.filter(account_type=account_obj, user=user).exists():
            raise serializers.ValidationError({
                "account_type": "This account type already exists"
            })
            
        attrs['account_obj'] = account_obj
        return attrs
    
    def create(self, validated_data):
        user = self.context.get('user')
        account_obj = validated_data.pop('account_obj')
        name = validated_data.pop('account_name')
        
        if not account_obj:
            account_obj = AccountBase.objects.create(name=name)
            
        return Account.objects.create(
            user=user, 
            account_type=account_obj, 
            **validated_data
        )
        
class TransactionTypeSerializer(serializers.Serializer):
    transaction_name = serializers.CharField(required=True, write_only=True)
    transaction_type = serializers.CharField(required=True, write_only=True)
        
    def validate(self, attrs):
        transaction_name = attrs.get('transaction_name')
        transaction_type = attrs.get('transaction_type')
        user = self.context.get('user')
        
        transaction_obj = TransactionTypeBase.objects.filter(name=transaction_name, type=transaction_type).first()
        if transaction_obj and TransactionTypePrivate.objects.filter(user=user, transaction_type=transaction_obj).exists():
            return field_error("transaction_type", "This transaction type already exists")
        
        attrs['transaction_obj'] = transaction_obj
        return attrs
    
    def create(self, validated_data):
        transaction_obj = validated_data.get('transaction_obj')
        user = self.context.get('user')
        
        if not transaction_obj:
            transaction_obj = TransactionTypeBase.objects.create(
                name=validated_data.get('transaction_name'),
                type=validated_data.get('transaction_type')
            )
            
        return TransactionTypePrivate.objects.create(user=user, transaction_type=transaction_obj)
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "transaction_name": instance.transaction_type.name,
            "transaction_type": instance.transaction_type.type,
        }
        
            
        
        