from django.contrib import admin
from .models import TempUser, MyToken

admin.site.register(TempUser)
admin.site.register(MyToken)