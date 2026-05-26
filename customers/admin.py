from django.contrib import admin
from .models import Customer

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "cif",
        "email",
        "phone",
        "is_active",
    )

    search_fields = (
        "name",
        "cif",
        "email",
    )

    list_filter = (
        "is_active",
    )

