from django.urls import path
from .views import (
    AccountCreateListAPIView, 
    TransactionTypeCreateListAPIView,
    transactiontype_delete_api_view, 
    account_delete_api_view
)

urlpatterns = [
    path('account', AccountCreateListAPIView.as_view()),
    path('account/<int:pk>', account_delete_api_view),
    
    path('transaction-type', TransactionTypeCreateListAPIView.as_view()),
    path('transaction-type/<int:pk>', transactiontype_delete_api_view),
]