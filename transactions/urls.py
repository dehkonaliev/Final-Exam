from django.urls import path
from .views import ListCreateTransactionAPIView

urlpatterns = [
    path('transaction', ListCreateTransactionAPIView.as_view()),
]