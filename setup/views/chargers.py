from django.contrib import messages
from django.views.generic import TemplateView

from charging_cost.rest import RestClient, RestError, RestResponse
from history.models import Charger


class ChargersView(TemplateView):
    template_name = 'chargers.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        try:
            chargers = []
            response = RestClient.chargers(self.request.user.token)
            for json in response.get(RestResponse.DATA):
                charger = Charger(
                    id=json.get("Id"),
                    name=json.get("Name"),
                    is_online=json.get("IsOnline"),
                    device_id=json.get("DeviceId"),
                    operating_mode=json.get("OperatingMode"),
                    created=json.get("CreatedOnDate"),
                    circuit_id=json.get("CircuitId"),
                    active=json.get("Active"),
                    pin=json.get("Pin"),
                    device_type=json.get("DeviceType"),
                    installation_id=json.get("InstallationId"),
                    installation_name=json.get("InstallationName"),
                    authorization_required=json.get("IsAuthorizationRequired")
                )
                chargers.append(charger)
            Charger.objects.bulk_create(
                chargers,
                update_conflicts=True,
                update_fields=['active', 'is_online', 'authorization_required', 'pin'],
                unique_fields=['id']
            )
            context['chargers'] = chargers
        except RestError:
            messages.add_message(self.request, messages.ERROR, "Błąd przy wczytywaniu urządzeń.")
        return context
