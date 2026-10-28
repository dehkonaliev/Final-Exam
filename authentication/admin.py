from django.contrib import admin
from .models import TempUser, MyToken, CustomUser

admin.site.register(TempUser)
admin.site.register(MyToken)
admin.site.register(CustomUser)