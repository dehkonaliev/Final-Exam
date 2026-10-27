from django.contrib import admin
from .models import Account, AccountBase, TransactionTypeBase, TransactionTypePrivate

admin.site.register(Account)
admin.site.register(AccountBase)
admin.site.register(TransactionTypePrivate)
admin.site.register(TransactionTypeBase)
