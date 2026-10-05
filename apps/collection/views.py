from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from .models import CollectionFollowUp


class CollectionFollowUpCancelView(LoginRequiredMixin, View):

    def post(self, request, pk):

        follow_up = get_object_or_404(
            CollectionFollowUp,
            pk=pk,
        )

        if follow_up.status != CollectionFollowUp.Status.ACTIVE:
            messages.error(
                request,
                "Este seguimiento ya no está activo."
            )

            return redirect(
                "accounts:account_detail",
                pk=follow_up.account.pk,
            )

        follow_up.status = CollectionFollowUp.Status.CANCELED
        follow_up.save(update_fields=["status"])

        messages.success(
            request,
            "El seguimiento de cobro se ha cancelado correctamente."
        )

        return redirect(
            "accounts:account_detail",
            pk=follow_up.account.pk,
        )
