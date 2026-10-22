from django.db import transaction
from apps.accounts.models import Account

from django.core.exceptions import ValidationError


@transaction.atomic
def register_new_account(
    *,
    customer,
    season,
    name,
    notes="",
):
    account = Account.objects.create(
        customer=customer,
        season=season,
        name=name,
        notes=notes,
    )

    return account

class AccountCloseService:

    @staticmethod
    def close(account):

        # 1. Comprobar si la cuenta ya está cerrada
        if account.is_closed:
            raise ValidationError("La cuenta seleccionada ya está cerrada actualmente.")

        # 2. Comprobar si el saldo es distinto de cero
        if account.balance != 0:
            raise ValidationError("No se puede cerrar una cuenta con saldo pendiente de regular.")

        # 3. Cambiar el estado de la cuenta
        account.is_closed = True


        # 4. Guardar los cambios en la base de datos
        account.save(update_fields=["is_closed"])

        return account
