from decimal import Decimal

from django.db import models

from accounts.models import Account

from django.core.exceptions import ValidationError
# Create your models here.

class Transaction(models.Model):

    class MovementType(models.TextChoices):
        CHARGE = "charge", "Cargo"
        PAYMENT = "payment", "Pago"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Efectivo"
        TRANSFER = "transfer", "Transferencia"
        BIZUM = "bizum", "Bizum"
        CARD = "card", "Tarjeta"
        COMPENSATION = "compensation", "Compensación"

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Cuenta",  
    )

    movement_type = models.CharField(
        max_length=10,
        choices=MovementType.choices,
        verbose_name="Tipo de movimiento"   
    )

    date = models.DateField(
        verbose_name="Fecha",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Importe",
    )

    description = models.CharField(
        max_length=255,
        verbose_name="Descripción",
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        blank=True,
        null=True,
        verbose_name="Método de pago",
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
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ["date", "id"]

    def __str__(self):
        return (
            f"{self.account.customer.name} - "
            f"{self.get_movement_type_display()} - "
            f"{self.amount}€"
        )
    
    @property
    def signed_amount(self):
        """
        Devuelve importe positivo o negativo
        según el tipo de movimiento. 
        """
        if self.movement_type == self.MovementType.CHARGE:
            return self.amount
        
        return -self.amount
    
    def clean(self):
        # => Si es un cargo no debe tener método de pago
        if (
            self.movement_type == self.MovementType.CHARGE
            and self.payment_method
        ):
            raise ValidationError({
                "payment_method":
                "Un cargo no puede tener método de pago"
            })
        
        # Si es un pago debe tener método de pago
        if (
            self.movement_type == self.MovementType.PAYMENT
            and not self.payment_method
        ):
            raise ValidationError({
                "payment_method":
                "Debe indicar un método de pago"
            })
        
        # El importe debe ser positvio
        if self.amount <=0:
            raise ValidationError({
                "amount":
                "El importe debe ser mayor que cero"
            })
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)