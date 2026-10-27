from django.urls import path
from .views import ListCreateTransactionAPIView, transfertome_api_view, transaction_history

urlpatterns = [
    path('transaction', ListCreateTransactionAPIView.as_view()),
    path('transaction/tome', transfertome_api_view),
    path('transaction/history', transaction_history),
]