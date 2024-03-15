from django.urls import path

from setup.views.chargers import ChargersView
from setup.views.history import HistoryView
from setup.views.price import PriceView
from setup.views.start import StartView

urlpatterns = [
    path("", StartView.as_view(), name="wizard_start"),
    path("urzadzenia/", ChargersView.as_view(), name="wizard_chargers"),
    path("historia/", HistoryView.as_view(), name="wizard_history"),
    path("cena/", PriceView.as_view(), name="wizard_price")
]
