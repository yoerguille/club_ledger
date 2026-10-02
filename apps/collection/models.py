from django.db import models

# Create your models here.
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.accounts.models import Account


class CollectionFollowUp(models.Model):

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="collection_followups",
        verbose_name="Cuenta",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Importe",
    )

    sent_at = models.DateTimeField(
        verbose_name="Fecha de envío",
    )

    due_date = models.DateField(
        verbose_name="Fecha de vencimiento",
    )

    is_closed = models.BooleanField(
        default=False,
        verbose_name="Cerrado",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Seguimiento de cobro"
        verbose_name_plural = "Seguimientos de cobro"
        ordering = ["-sent_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["account"],
                condition=models.Q(is_closed=False),
                name="unique_active_follow_up_per_account"
            )
        ]

    def __str__(self):
        return (
            f"{self.account.customer.name} - "
            f"{self.amount} € - "
            f"{self.sent_at:%d/%m/%Y}"
        )

    def clean(self):
        if self.amount <= Decimal("0.00"):
            raise ValidationError({
                "amount": "El importe debe ser mayor que cero."
            })

        if not self.is_closed:
            active_follow_up = CollectionFollowUp.objects.filter(
                account=self.account,
                is_closed=False,
            ).exclude(
                pk=self.pk,
            ).exists()

            if active_follow_up:
                raise ValidationError(
                    "Esta cuenta ya tiene un seguimiento de cobro activo."
                )