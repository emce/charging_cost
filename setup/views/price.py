from django import forms
from django.core.validators import MinValueValidator
from django.urls import reverse_lazy
from django.views.generic import FormView

from history.cost import Cost
from history.models import EnergyCost


class PriceForm(forms.Form):
    type = forms.ChoiceField(choices={
        (Cost.G11.value, Cost.G11.name),
        (Cost.G12.value, Cost.G12.name),
        (Cost.G12W.value, Cost.G12W.name)
    })
    price_day = forms.FloatField(required=True, initial=0.0, validators=[MinValueValidator(0.1)])
    price_night = forms.FloatField(required=True, initial=0.0, validators=[MinValueValidator(0.1)])


class PriceView(FormView):
    template_name = 'price.html'
    form_class = PriceForm

    def get_success_url(self):
        return reverse_lazy("history_index")

    def form_valid(self, form):
        cost = EnergyCost.objects.create(
            user=self.request.user,
            tariff=form.cleaned_data.get("type"),
            price_day=form.cleaned_data.get("price_day"),
            price_night=form.cleaned_data.get("price_night")
        )
        cost.save()
        return super().form_valid(form)
