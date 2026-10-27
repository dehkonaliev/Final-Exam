from django.db import models
from accounting.models import TransactionTypeBase, Account

class Transaction(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    transaction_type = models.ForeignKey(TransactionTypeBase, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')