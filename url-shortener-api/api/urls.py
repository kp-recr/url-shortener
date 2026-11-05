from django.urls import path

from . import views

urlpatterns = [
    path(
        "short-urls/",
        views.create_short_url,
        name="short-url-create",
    ),
]
