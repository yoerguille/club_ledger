from django.db import models

# Create your models here.
class Season(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Temporada",       
    )

    start_date = models.DateField(
        verbose_name="Fecha de inicio",
    )

    end_date = models.DateField(
        verbose_name="Fecha fin",
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name="Activa",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        ordering = ["-start_date"]

    def __str__(self):
        return self.name