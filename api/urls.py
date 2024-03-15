from django.urls import path

from api.views import login, chargers, history
from charging_cost.rest import RestUrl

urlpatterns = [
    path("", login, name='api_start'),
    path(RestUrl.AUTH, login, name='api_login'),
    path(RestUrl.CHARGERS, chargers, name='api_chargers'),
    path(RestUrl.HISTORY, history, name='api_history'),
]
