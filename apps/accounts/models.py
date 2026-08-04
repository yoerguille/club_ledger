from django.db import models
from apps.customers.models import Customer
from apps.seasons.models import Season
from decimal import Decimal


# Create your models here.

class Account(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="accounts",
        verbose_name="Cliente",
    )

    season = models.ForeignKey(
        Season,
        on_delete=models.PROTECT,
        related_name="accounts",
        verbose_name="Temporada",
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["customer", "season"],
                name="unique_customer_season_account"
            )
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.season.name}"
    
    @property
    def balance(self):
        total = Decimal("0.00")
        """
        Calcula el saldo actual de la cuenta
        """
        for transaction in self.transactions.all():
            total += transaction.signed_amount

        return total

    @property
    def total_charges(self):
        from apps.transactions.models import Transaction
        total = Decimal("0.00")
        """
        Calcula el total de pedidos
        """
        for transaction in self.transactions.filter(
            movement_type=Transaction.MovementType.CHARGE
        ):
            total += transaction.amount

        return total

    @property
    def total_payments(self):
        from apps.transactions.models import Transaction
        total = Decimal("0.00")
        """
        Calcula el total de pagos
        """
        for transaction in self.transactions.filter(
            movement_type=Transaction.MovementType.PAYMENT
        ):
            total += transaction.amount

        return total
    