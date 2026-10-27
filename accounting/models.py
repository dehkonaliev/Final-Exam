from django.db import models
from django.contrib.auth.models import User


class AccountBase(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Account(models.Model):
    class CurrencyTypes(models.TextChoices):
        USD = "USD", 'usd'
        SUM = "SUM", 'sum'
        RUBL = "RUBL", 'rubl'
        EURO = "EURO", 'euro'
        
    account_type = models.ForeignKey(AccountBase, null=True, blank=True, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    currency = models.CharField(max_length=20, choices=CurrencyTypes.choices, default=CurrencyTypes.SUM)
    
    def __str__(self):
        return f"{self.user.username} - {self.account_type}"
    
    class Meta:
        unique_together = [
            'user', 'account_type'
        ]
    
class TransactionTypeBase(models.Model):
    class TransactionTypes(models.TextChoices):
        INCOME = "INCOME", 'income'
        OUTCOME = "OUTCOME", 'outcome'
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TransactionTypes.choices)
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ['name', 'type']
    
class TransactionTypePrivate(models.Model):
    transaction_type = models.ForeignKey(TransactionTypeBase, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    
