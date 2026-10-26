from django.core.exceptions import ValidationError
from django.db import connection, transaction

from apps.seasons.models import Season
from apps.seasons.services.season_stats import get_season_pending_balances


class SeasonChangeConfirmationRequired(Exception):
    """Se necesita confirmar la sustitución de la temporada activa."""

    def __init__(self, summary):
        self.summary = summary
        super().__init__("Debes confirmar el cambio de temporada.")

class SeasonService:

    @staticmethod
    def get_active_season():
        return Season.objects.filter(is_active=True).first()

    @staticmethod
    def get_change_summary():
        """Devuelve información para mostrar el aviso de confirmación."""

        active_season = SeasonService.get_active_season()

        if active_season is None:
            return None

        pending = get_season_pending_balances(active_season)

        return {
            "season_name": active_season.name,
            "pending_accounts_count": pending["pending_accounts_count"],
            "total_pending": pending["total_pending"],
        }

    @staticmethod
    def create_season(
        *,
        name,
        start_date,
        end_date,
        confirm_change=False,
        expected_active_season_id=None,
    ):
        with transaction.atomic():

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT pg_advisory_xact_lock(%s)",
                    [824731],
                )

            active_season = Season.objects.filter(
                is_active=True
            ).first()

            # 1. Exigir confirmación
            if active_season and not confirm_change:
                summary = {
                    "season_id": active_season.pk,
                    "season_name": active_season.name,
                    **get_season_pending_balances(active_season),
                }

                raise SeasonChangeConfirmationRequired(summary)

            # 2. Comprobar que se confirmó la temporada correcta
            if confirm_change:
                if (
                    active_season is None
                    or str(active_season.pk) != str(expected_active_season_id)
                ):
                    raise ValidationError(
                        "La temporada activa ha cambiado. "
                        "Debes confirmar nuevamente la operación."
                    )
            if end_date <= start_date:
                raise ValidationError({
                    "end_date": "La fecha de finalización debe ser posterior a la fecha de inicio."
                })

            # 3. Validar, desactivar la anterior y crear la nueva
            season = Season(
                name=name,
                start_date=start_date,
                end_date=end_date,
                is_active=True,
            )

            season.full_clean(validate_constraints=False)

            Season.objects.filter(is_active=True).update(is_active=False)

            season.save()

            return season