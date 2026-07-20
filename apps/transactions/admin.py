from django.contrib import admin
from .models import Transaction
# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "account",
        "movement_type",
        "date",
        "amount",
        "payment_method",
    )

    search_fields = (
        "description",
        "account__customer__name",
    )

    list_filter = (
        "movement_type",
        "payment_method",
        "date",
    )
    
    ordering = (
        "-date",
    )

