from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from apps.accounts.models import Account
from apps.transactions.serializers import PaymentSerializer
from apps.transactions.services import register_payment


class PaymentCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, account_pk):
        # 1. Comprobar permisos
        if not request.user.has_perm("transactions.add_transaction"):
            return Response(
                {"detail": "No tienes permiso para registrar pagos."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 2. Recuperar la cuenta
        account = get_object_or_404(Account, pk=account_pk)

        # 3. Validar los datos
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 4. Registrar el pago
        payment = register_payment(
            account=account,
            **serializer.validated_data,
        )

        # 5. Devolver la respuesta HTTP
        return Response(
            {
                "id": payment.pk,
                "account": account.pk,
                "amount": str(payment.amount),
                "message": "Pago registrado correctamente.",
            },
            status=status.HTTP_201_CREATED,
        )