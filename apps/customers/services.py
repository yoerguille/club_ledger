from django.db import transaction
from apps.customers.models import Customer

@transaction.atomic
def register_customer(
    *,
    name,
    cif,
    email,
    phone,
    adress="",
    contact_person,
):
    customer = Customer.objects.create(
        name=name,
        cif = cif,
        email=email,
        phone=phone,
        adress=adress,
        contact_person=contact_person,
    )

    return customer