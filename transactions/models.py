from django.db import models
from accounting.models import TransactionTypeBase, Account

class Transaction(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    transaction_type = models.ForeignKey(TransactionTypeBase, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_balance = models.DecimalField(blank=True, default=0)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    
    def save(self, *args, **kwargs):
        if not self.changed_balance:
            if self.transaction_type.type == self.transaction_type.TransactionTypes.INCOME:
                self.changed_balance = self.account.balance + self.amount
            elif self.transaction_type.type == self.transaction_type.TransactionTypes.EXPENCE:
                self.changed_balance = self.account.balance - self.amount
        return super().save()