from django.urls import path

from . import views


app_name = "collection"


urlpatterns = [
    path(
        "<int:pk>/cancel/",
        views.CollectionFollowUpCancelView.as_view(),
        name="follow_up_cancel",
    ),
    path(
        "<int:pk>/prepare-reminder/",
        views.CollectionReminderPrepareView.as_view(),
        name="prepare_reminder",
    ),
    path(
    "<int:pk>/send-reminder/",
    views.CollectionReminderSendView.as_view(),
    name="send_reminder",
),
]