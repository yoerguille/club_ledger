from django.urls import path
from .views import SeasonCreateView, SeasonListView

app_name = 'seasons'

urlpatterns = [
    path("create/", SeasonCreateView.as_view(), name="season_create"),
    path("list/", SeasonListView.as_view(), name="season_list"),
]
