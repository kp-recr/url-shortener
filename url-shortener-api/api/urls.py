from django.urls import path

from . import views

urlpatterns = [
    path(
        "short-urls/",
        views.create_short_url,
        name="short-url-create",
    ),
    path(
        "short-urls/resolve/",
        views.resolve_short_url,
        name="short-url-resolve",
    ),
    path(
        "short-urls/<str:key>/",
        views.resolve_short_url_by_key,
        name="short-url-resolve-by-key",
    ),
]
