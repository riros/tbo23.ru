from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class AccountInLine(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = "accounts"

class UserAdmin(BaseUserAdmin):
    inlines = (AccountInLine,)

admin.site.register(UserAdmin)
