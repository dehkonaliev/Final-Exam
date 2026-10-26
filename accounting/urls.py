from django.urls import path
from .views import AccountCreateListAPIView

urlpatterns = [
    path('account', AccountCreateListAPIView.as_view())
]