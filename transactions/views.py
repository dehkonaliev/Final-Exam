from django.shortcuts import render
from .models import Transaction
from .serializers import TransactionSerializer
from authentication.utils import success_response, error_response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class ListCreateTransactionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TransactionSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Transaction created", data=serializer.data)
    
    def get(self, request):
        transactions = Transaction.objects.filter(account__user=request.user).order_by('-created_at')
        
        return success_response(message="Transaction list", data=TransactionSerializer(transactions, many=True).data)