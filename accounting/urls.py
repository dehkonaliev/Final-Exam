from django.urls import path
from .views import AccountCreateListAPIView, TransactionTypeCreateListAPIView

urlpatterns = [
    path('account', AccountCreateListAPIView.as_view()),
    path('transaction_type', TransactionTypeCreateListAPIView.as_view()),
]