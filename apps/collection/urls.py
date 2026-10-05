from django.urls import path

from . import views


app_name = "collection"


urlpatterns = [
    path(
        "<int:pk>/cancel/",
        views.CollectionFollowUpCancelView.as_view(),
        name="follow_up_cancel",
    ),
]