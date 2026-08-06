from decimal import Decimal
from apps.transactions.models import Transaction

class StatementBuilder:
    def __init__(self, account):
        self.account = account

    def build(self):
        running_balance = Decimal("0.00")
        rows = []

        transactions = (
            self.account.transactions
            .select_related()
            .order_by("date", "pk")
        )

        for transaction in transactions:

            running_balance += transaction.signed_amount

            rows.append({
                "transaction":transaction,
                "running_balance":running_balance,
            })

        return {
            "account": self.account,
            "customer": self.account.customer,
            "season": self.account.season,
            "rows": rows,
            "total_charges": self.account.total_charges,
            "total_payments": self.account.total_payments,
            "balance": running_balance,
        }