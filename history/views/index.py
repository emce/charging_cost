from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from history.cost import get_cost_by_value
from history.models import History, Charger, EnergyCost


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('wizard_start'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        energy_sum = round(History.objects.aggregate(Sum('energy'))['energy__sum'], 2)
        energy_cost = EnergyCost.objects.get(user=self.request.user)
        cost = get_cost_by_value(energy_cost.tariff)
        total_cost = 0
        for item in History.objects.all():
            total_cost += cost.price(item.start, energy_cost.price_day, energy_cost.price_night) * item.energy
        context = TemplateView.get_context_data(self, **kwargs)
        context['total_energy'] = energy_sum
        context['total_charging'] = History.objects.all().count()
        context['chargers'] = Charger.objects.all().count()
        context['total_cost'] = round(total_cost, 2)
        return context
