from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import UpdateView, DetailView, CreateView, ListView
from apps.seasons.models import Season
from apps.seasons.forms import SeasonForm
from apps.seasons.services.season_service import (
    SeasonService,
    SeasonChangeConfirmationRequired,
)
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse
from apps.seasons.services.season_stats import get_season_stats

# Create your views here.
class SeasonUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Season
    form_class = SeasonForm
    template_name = "seasons/forms/season_form.html"
    permission_required="seasons.change_season"

    def form_valid(self, form):
        self.object = form.save()

        return JsonResponse({
            "success": True,
            "message": "Temporada actualizada correctamente.",
            "season": {
                "id": self.object.pk,
                "name": self.object.name,
                "start_date": self.object.start_date.strftime("%d/%m/%Y"),
                "end_date": self.object.end_date.strftime("%d/%m/%Y"),
            },
        }, status=200)

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "errors": form.errors.get_json_data(),
        }, status=400)


class SeasonListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Season
    template_name = "seasons/season_list.html"
    context_object_name = "seasons"
    permission_required="seasons.view_season"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        seasons = list(context["seasons"])

        for season in seasons:
            season.card_stats = get_season_stats(season)

            # Formulario precargado con los datos de esta temporada
            season.edit_form = SeasonForm(instance=season)

        context["seasons"] = seasons
        context["season_form"] = SeasonForm()

        return context

class SeasonCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Season
    context_object_name = "season"
    template_name = "seasons/forms/season_form.html"
    form_class=SeasonForm
    permission_required="seasons.add_season"

    def form_valid(self, form):
        confirm_change = (
            self.request.POST.get("confirm_change") == "true"
        )

        expected_active_season_id = self.request.POST.get(
            "expected_active_season_id"
        )
        try:
            self.get_object = SeasonService.create_season(
                name = form.cleaned_data['name'],
                start_date= form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                confirm_change=confirm_change,
                expected_active_season_id=expected_active_season_id,
            )
        except SeasonChangeConfirmationRequired as error:
            return JsonResponse({
                "success": False,
                "requires_confirmation": True,
                "season": {
                    "id": error.summary["season_id"],
                    "name": error.summary["season_name"],
                    "pending_accounts_count": error.summary["pending_accounts_count"],
                    "total_pending": str(error.summary["total_pending"]),
                },
            }, status=409)

        except ValidationError as e:
            for message in e.messages:
                form.add_error(None, message)

            return self.form_invalid(form)


        messages.success(
            self.request,
            "La temporada se ha creado correctamente"
        )

        return JsonResponse({
                    "success": True,
                    "message": "Nuevo temporada creada correctamente.",
                }, status=201)

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "errors": form.errors.get_json_data()
        }, status=400)
