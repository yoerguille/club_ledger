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

    if not active_season:
        return {
            "total_customers" : total_customers,
            "active_season" : None,
            "total_accounts" : 0,
            "total_transactions" : 0,
            "total_payments" : 0,
            "total_charges" : 0,
            "total_balance" : 0,
        }

    accounts = Account.objects.filter(
        season = active_season
    )

    transactions = Transaction.objects.filter(
        account__season = active_season
    )

    total_accounts = accounts.count()

    total_transactions = transactions.count()

    total_charges = transactions.filter(
        movement_type = Transaction.MovementType.CHARGE
    ).aggregate(
        total=Coalesce(
            Sum("amount"),
            Value(0),
            output_field=DecimalField(
                max_digits=12,
                decimal_places=2
            ),
        )
    )["total"]

    total_payments = transactions.filter(
        movement_type = Transaction.MovementType.PAYMENT
    ).aggregate(
        total=Coalesce(
            Sum("amount"),
            Value(0),
            output_field=DecimalField(
                max_digits=12,
                decimal_places=2
            ),
        )
    )["total"]

    total_balance = (
        transactions.aggregate(
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
        "total_accounts" : total_accounts,
        "total_transactions" : total_transactions,
        "total_payments" : total_payments,
        "total_charges" : total_charges,
        "total_balance" : total_balance,
    }