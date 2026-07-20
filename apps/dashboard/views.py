from django.shortcuts import render
from django.views.generic import TemplateView

from .services import get_dashboard_stats

# Create your views here.

class DashboardView(TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(get_dashboard_stats())
        
        return context
    
