from django.db.models import Case, DecimalField, F, Sum, Value, When
from django.db.models.functions import Coalesce

from apps.accounts.models import Account
from apps.customers.models import Customer
from apps.seasons.models import Season
from apps.transactions.models import Transaction


def get_dashboard_stats():

    """
    Mostrará las estadísticas de las cuentas.

    """

    total_customers = Customer.objects.filter(is_active = True).count()

    active_season = Season.objects.filter(is_active = True).first()

    total_transactions = Transaction.objects.count()

    total_balance = (
        Transaction.objects.aggregate(
            balance=Coalesce(
                Sum(
                    Case(
                        When(
                            movement_type=Transaction.MovementType.CHARGE,
                            then=F("amount"),
                        ),
                        When(
                            movement_type=Transaction.MovementType.PAYMENT,
                            then=-F("amount"),
                        ),
                        output_field=DecimalField(
                            max_digits=12,
                            decimal_places=2,
                        ),
                    )
                ),
                Value(0),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2,
                ),
            )
        )["balance"]
    )


    return {
        "total_customers" : total_customers,
        "active_season" : active_season,
        "total_transactions" : total_transactions,
        "total_balance" : total_balance,
    }