from django.shortcuts import render
from .models import Transaction
from accounting.models import TransactionTypeBase, Account
from .serializers import TransactionSerializer, TransferToMeSerializer
from authentication.utils import success_response, error_response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta, datetime
from .paginations import StandardPagination
from django.db.models import Sum



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

interval_delta = {
    'daily': datetime.now() - timedelta(hours=24),
    'weekly': datetime.now() - timedelta(days=7),
    'monthly': datetime.now() - timedelta(days=30)
}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-created_at')
    interval = request.query_params.get('interval')
    max_amount = request.query_params.get('max_amount')
    min_amount = request.query_params.get('min_amount')
    transaction_type = request.query_params.get('transaction_type')
    inout = request.query_params.get('inout')
    account = request.query_params.get('account')
    
    applied_filters = {}
    
    if interval and interval in interval_delta.keys():
        transactions = transactions.filter(created_at__gt=interval_delta[interval])
        applied_filters['interval'] = interval
    try:
        if max_amount and min_amount:
            transactions = transactions.filter(amount__gte=min_amount, amount__lte=max_amount)
            applied_filters['min_amount'] = min_amount
            applied_filters['max_amount'] = max_amount
            
        elif max_amount and not min_amount:
            transactions = transactions.filter(amount__lte=max_amount)
            applied_filters['max_amount'] = max_amount
            
        elif not max_amount and min_amount:
            transactions = transactions.filter(amount__gte=min_amount)
            applied_filters['min_amount'] = min_amount
            
    except:
        return error_response(message="max_amount and min_amount must be Decimal values")
    
    if transaction_type:
        try:
            transaction_type = int(transaction_type)
            transaction_type_obj = TransactionTypeBase.objects.get(id=transaction_type)
            
            transactions = transactions.filter(transaction_type=transaction_type_obj)
            applied_filters['transaction_type'] = {
                "name": transaction_type_obj.name,
                "type": transaction_type_obj.type
            }
        except TransactionTypeBase.DoesNotExist:
            return error_response(message="transaction_type not found", status_code=404)
        
    if inout and inout in TransactionTypeBase.TransactionTypes.values:
        transactions = transactions.filter(transaction_type__type=inout)
        applied_filters['inout'] = inout
        
    if account:
        try:
            account = Account.objects.filter(id=account).first()
            if not account:
                return error_response(message="Account not found")
            transactions = transactions.filter(account=account)
            applied_filters['account'] = account.account_type.name
        except Exception as err:
            return error_response(message=str(err))
    
    paginator = StandardPagination()
    
    page = paginator.paginate_queryset(transactions, request)
    
    total_expence = transactions.filter(transaction_type__type='EXPENCE').aggregate(Sum('amount'))['amount__sum']   
    total_income = transactions.filter(transaction_type__type='INCOME').aggregate(Sum('amount'))['amount__sum']    
    
    response = {
        "count": transactions.count(),
        "applied_filters":applied_filters,
        "total_income": total_income,
        "total_expence": total_expence,
        'transactions': TransactionSerializer(page, many=True).data
    }
    
    return success_response(message="Transaction history", data=response)
    