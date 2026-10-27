from django.db.models import (
    Case, DecimalField,Q, F, Sum, Value, When
)
from django.db.models.functions import Coalesce

from apps.accounts.models import Account
from apps.transactions.models import Transaction

from decimal import Decimal

from django.db.models import Sum

from apps.accounts.models import Account
from apps.transactions.models import Transaction

from decimal import Decimal

from django.db.models import Q, Sum

from apps.accounts.models import Account
from apps.transactions.models import Transaction


def get_season_stats(season):
    """
    Calcula las estadísticas económicas de una temporada.

    Funciona tanto para temporadas activas como inactivas.
    """

    transactions = Transaction.objects.filter(
        account__season=season
    )

    # Agrupar los importes por tipo de movimiento
    totals = transactions.aggregate(
        total_charges=Sum(
            "amount",
            filter=Q(
                movement_type=Transaction.MovementType.CHARGE
            ),
        ),
        total_payments=Sum(
            "amount",
            filter=Q(
                movement_type=Transaction.MovementType.PAYMENT
            ),
        ),
    )

    total_charges = totals["total_charges"] or Decimal("0.00")
    total_payments = totals["total_payments"] or Decimal("0.00")

    # Reutilizar la lógica existente de saldos pendientes
    pending = get_season_pending_balances(season)

    return {
        "account_count": Account.objects.filter(
            season=season
        ).count(),

        "transaction_count": transactions.count(),

        "total_charges": total_charges,
        "total_payments": total_payments,

        "total_balance": total_charges - total_payments,

        "pending_accounts_count": pending["pending_accounts_count"],
        "total_pending": pending["total_pending"],
    }

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