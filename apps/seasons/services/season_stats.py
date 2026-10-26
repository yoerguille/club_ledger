from django.db.models import (
    Case, DecimalField, F, Sum, Value, When
)
from django.db.models.functions import Coalesce

from apps.accounts.models import Account
from apps.transactions.models import Transaction


def get_season_pending_balances(season):
    accounts = Account.objects.filter(
        season=season
    ).annotate(
        balance=Coalesce(
            Sum(
                Case(
                    When(
                        transactions__movement_type=Transaction.MovementType.CHARGE,
                        then=F("transactions__amount"),
                    ),
                    When(
                        transactions__movement_type=Transaction.MovementType.PAYMENT,
                        then=-F("transactions__amount"),
                    ),
                    output_field=DecimalField(
                        max_digits=12,
                        decimal_places=2,
                    ),
                )
            ),
            Value(
                0,
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2,
                ),
            ),
        )
    )

    pending_accounts = accounts.filter(balance__gt=0)

    return pending_accounts.aggregate(
        total_pending=Coalesce(
            Sum("balance"),
            Value(
                0,
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2,
                ),
            ),
        ),
        # Cantidad de cuentas con deuda
    ) | {
        "pending_accounts_count": pending_accounts.count()
    }