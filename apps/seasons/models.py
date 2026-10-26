from django.db import models
from django.db.models import Q, F

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
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        ordering = ["-start_date"]

        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__gt=F("start_date")),
                name="season_end_after_start",
            ),
            models.UniqueConstraint(
                fields=["is_active"],
                condition=Q(is_active=True),
                name="unique_active_season",
            ),
        ]

    def __str__(self):
        return self.name