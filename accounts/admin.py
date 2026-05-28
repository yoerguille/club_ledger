from django.contrib import admin
from .models import Account
# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "season",
        "get_balance",
        "created_at",
    )

    search_fields = (
        "customer__name",
    )

    list_filter = (
        "season",
    )

    def get_balance(self, obj):
        return f"{obj.balance} €"
    
    get_balance.short_description = "Saldo"
