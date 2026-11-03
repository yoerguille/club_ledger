from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from apps.seasons.models import Season
from apps.customers.models import Customer
from apps.accounts.serializers import AccountSerializer
from apps.accounts.services import register_new_account
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class AccountCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, customer_pk):
        # 1. Comprobar permisos
        if not request.user.has_perm("accounts.add_account"):
            return Response(
                {"detail": "No tienes permiso para registrar una nueva cuenta."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 2. Recuperar el customer y la season activa
        customer = get_object_or_404(Customer, pk=customer_pk)
        season = Season.objects.filter(is_active=True).first()

        if not season:
            return Response(
                {"detail": "No hay ninguna temporada activa. Por favor, cree una temporada antes de crear una cuenta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. Validar los datos
        serializer = AccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 4. Registrar la nueva cuenta
        account = register_new_account(
            customer=customer,
            season=season,
            **serializer.validated_data,
        )

        # 5. Devolver la respuesta HTTP
        return Response(
            {
                "id": account.pk,
                "customer": customer.pk,
                "name": account.name,
                "message": "Cuenta registrada correctamente.",
            },
            status=status.HTTP_201_CREATED,
        )
