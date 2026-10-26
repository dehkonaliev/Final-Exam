from rest_framework import serializers
from .models import TransactionTypeBase, TransactionTypePrivate, Transaction, AccountBase, Account
from authentication.utils import field_error


class AccountBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBase
        fields = ['id', 'name']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        name = validated_data['name']
        account_obj = AccountBase.objects.filter(name=name).first()
        if account_obj:
            return account_obj
        return AccountBase.objects.create(name=name)
    

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