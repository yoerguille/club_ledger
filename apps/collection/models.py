from django.db import models

# Create your models here.
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.accounts.models import Account

from django.utils import timezone


class CollectionFollowUp(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        COMPLETED = "completed", "Completo"
        CANCELED = "canceled", "Cancelado" 

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

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Estado",
    )

    sent_at = models.DateTimeField(
        verbose_name="Fecha de envío",
    )

    due_date = models.DateField(
        verbose_name="Fecha de vencimiento",
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
                condition=models.Q(status="active"),
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

        if self.status == self.Status.ACTIVE:
            active_follow_up = CollectionFollowUp.objects.filter(
                account=self.account,
                status = self.Status.ACTIVE,
            ).exclude(
                pk=self.pk,
            ).exists()

            if active_follow_up:
                raise ValidationError(
                    "Esta cuenta ya tiene un seguimiento de cobro activo."
                )

    @property
    def is_overdue(self):
        return (
            self.status == self.Status.ACTIVE
            and self.due_date < timezone.localdate()
        )

    @property
    def days_overdue(self):
        if not self.is_overdue:
            return 0

        return (timezone.localdate() - self.due_date).days


class CollectionReminder(models.Model):

    follow_up = models.ForeignKey(
        CollectionFollowUp,
        on_delete=models.PROTECT,
        related_name="reminders",
        verbose_name="Seguimiento de cobro",
    )

    recipient_email = models.EmailField(
        verbose_name="Email destinatario",
    )

    subject = models.CharField(
        max_length=255,
        verbose_name="Asunto",
    )

    message = models.TextField(
        verbose_name="Mensaje enviado",
    )

    balance_at_send = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Saldo en el momento del envío",
    )

    sent_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de envío",
    )

    class Meta:
        verbose_name = "Recordatorio de cobro"
        verbose_name_plural = "Recordatorios de cobro"
        ordering = ["-sent_at"]

    def __str__(self):
        return (
            f"Recordatorio - "
            f"{self.follow_up.account.customer.name} - "
            f"{self.sent_at:%d/%m/%Y}"
        )