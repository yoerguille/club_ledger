from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Nombre"
    )

    cif = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name="CIF",
    )

    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Correo electrónico"
    )

    phone = models.CharField(
        blank=True,
        null=True,
        max_length=9,
        verbose_name="Nº Teléfono"
    )

    adress = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dirección',
    )

    contact_person = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Persona de contacto'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',            
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ["name"]

    def __str__(self):
        return self.name