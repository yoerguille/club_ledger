from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.seasons.forms import SeasonForm

from .services import get_dashboard_stats
from apps.collection.services import get_overdue_follow_ups
from apps.dashboard.services import get_monthly_transactions, get_account_balance_distribution

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(get_dashboard_stats())

        context["overdue_follow_ups"] = get_overdue_follow_ups()

        context["season_form"] = SeasonForm()

        monthly_transactions = get_monthly_transactions(
            context["active_season"]
        )

        accounts_distribution = get_account_balance_distribution(
            context["active_season"]
        )
        
        context["monthly_chart_data"] = [
            {
                "month": item["month"].strftime("%Y-%m"),
                "charges": float(item["charges"]),
                "payments": float(item["payments"]),
            }
            for item in monthly_transactions
        ]
        context["accounts_distribution"] = accounts_distribution
        
        return context
    
