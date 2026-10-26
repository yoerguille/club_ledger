from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.seasons.forms import SeasonForm

from .services import get_dashboard_stats
from apps.collection.services import get_overdue_follow_ups

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(get_dashboard_stats())

        context["overdue_follow_ups"] = get_overdue_follow_ups()

        context["season_form"] = SeasonForm()
        
        return context
    
