from django.urls import path
from .views import SeasonCreateView

app_name = 'seasons'

urlpatterns = [
    path("create/", SeasonCreateView.as_view(), name="season_create"),
]
