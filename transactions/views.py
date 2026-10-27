from django.shortcuts import render
from .models import Transaction
from .serializers import TransactionSerializer, TransferToMeSerializer
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
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfertome_api_view(request):
    serializer = TransferToMeSerializer(data=request.data, context={'user': request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return success_response(message="Transfer is successfull", data=serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    pass
    