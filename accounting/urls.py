from django.urls import path
from .views import (
    AccountCreateListAPIView, 
    TransactionTypeCreateListAPIView,
    transactiontype_delete_api_view, 
    AccountEditDeleteAPIView
)

urlpatterns = [
    path('account', AccountCreateListAPIView.as_view()),
    path('account/<int:pk>', AccountEditDeleteAPIView.as_view()),
    
    path('transaction-type', TransactionTypeCreateListAPIView.as_view()),
    path('transaction-type/<int:pk>', transactiontype_delete_api_view),
]