from datetime import datetime, timedelta

from django.contrib import messages
from django.views.generic import TemplateView

from charging_cost.rest import RestClient, RestResponse, RestError
from charging_cost.settings import DATE_FORMAT
from history.models import History, Charger


class HistoryView(TemplateView):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        try:
            end = DATE_FORMAT.format(datetime.now())
            start = DATE_FORMAT.format(datetime.now() - timedelta(days=365))
            history = []
            for charger in Charger.objects.all():
                response = RestClient.charging_history(self.request.user.token,
                                                       charger.device_id, start, end)
                for json in response.get(RestResponse.DATA):
                    item = History(
                        id=json.get("Id"),
                        device_id=json.get("DeviceId"),
                        start=DATE_FORMAT.format(
                            datetime.strptime(json.get("StartDateTime"), "%Y-%m-%dT%H:%M:%S.%f")),
                        end=DATE_FORMAT.format(
                            datetime.strptime(json.get("EndDateTime"), "%Y-%m-%dT%H:%M:%S.%f")),
                        energy=json.get("Energy"),
                        charger_id=json.get("ChargerId"),
                        device_name=json.get("DeviceName")
                    )
                    history.append(item)
            History.objects.bulk_create(
                history,
                update_conflicts=True,
                update_fields=['start', 'end'],
                unique_fields=['id']
            )
            context['history'] = history
        except RestError:
            messages.add_message(self.request, messages.ERROR, "Błąd przy wczytywaniu historii ładowań.")
        return context
