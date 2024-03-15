from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from django.views.generic import TemplateView

from history.cost import get_cost_by_value
from history.models import History, EnergyCost


class DetailsView(TemplateView):
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        today = datetime.now()
        month = today.month
        year = today.year
        energy_cost = EnergyCost.objects.get(user=self.request.user)
        cost = get_cost_by_value(energy_cost.tariff)
        if "miesiac" in self.request.GET.keys():
            month = int(self.request.GET["miesiac"])
            year = int(self.request.GET["rok"])
        history_list = History.objects.filter(start__month=month, start__year=year).order_by('start')
        energy = 0.0
        total_cost = 0.0
        for item in history_list:
            energy += item.energy
            total_cost += cost.price(item.start, energy_cost.price_day, energy_cost.price_night) * item.energy
        current = date(year=year, month=month, day=1)
        context = TemplateView.get_context_data(self, **kwargs)
        context['current'] = current
        context['today'] = date(year=today.year, month=today.month, day=1)
        context['next'] = current + relativedelta(months=1)
        context['previous'] = current - relativedelta(months=1)
        context['history'] = history_list
        context['cost'] = cost
        context['price_day'] = energy_cost.price_day
        context['price_night'] = energy_cost.price_night
        context['total_energy'] = energy
        context['total_cost'] = total_cost
        return context
