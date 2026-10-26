from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import AccountSerializer, TransactionTypeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from authentication.utils import success_response
from .models import Account, AccountBase, TransactionTypePrivate


class AccountCreateListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AccountSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Account created", data=serializer.data)
    
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        
        return success_response(message="Your accounts", data=AccountSerializer(accounts, many=True).data)
    
    

class TransactionTypeCreateListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TransactionTypeSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="New transaction type created", data=serializer.data)
    
    def get(self, request):
        transaction_types = TransactionTypePrivate.objects.filter(user=request.user)
        
        return success_response(message="Your transaction types", data=TransactionTypeSerializer(transaction_types, many=True).data)