from django.urls import path

from .views.details import DetailsView
from .views.index import IndexView
from .views.settings import SettingsView

urlpatterns = [
    path("", IndexView.as_view(), name="history_index"),
    path("ustawienia", SettingsView.as_view(), name="history_settings"),
    path("szczegoly", DetailsView.as_view(), name="history_details"),
]
