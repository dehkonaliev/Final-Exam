from django.urls import path
from .views import ListCreateTransactionAPIView, transfertome_api_view

urlpatterns = [
    path('transaction', ListCreateTransactionAPIView.as_view()),
    path('transaction/tome', transfertome_api_view),
]