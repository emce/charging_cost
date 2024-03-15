from django import forms
from django.contrib import messages
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.views.generic import FormView

from charging_cost.rest import RestError, RestClient, RestResponse
from history.cost import Cost
from history.models import EnergyCost, ZaptecUser


class SettingsForm(forms.Form):
    type = forms.ChoiceField(choices={
        (Cost.G11.value, Cost.G11.name),
        (Cost.G12.value, Cost.G12.name),
        (Cost.G12W.value, Cost.G12W.name)
    })
    price_day = forms.FloatField(required=True, initial=0.0)
    price_night = forms.FloatField(required=True, initial=0.0)
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=5)
    repeat_password = forms.CharField(widget=forms.PasswordInput, min_length=5)

    def authorise(self, request: HttpRequest):
        return RestClient.auth(request.user.username, self.cleaned_data.get("new_password"))


class SettingsView(FormView):
    template_name = 'settings.html'
    form_class = SettingsForm

    def get_initial(self):
        initial = super(SettingsView, self).get_initial()
        cost = EnergyCost.objects.get(user_id=self.request.user.id)
        initial['type'] = cost.tariff
        initial['price_day'] = cost.price_day
        initial['price_night'] = cost.price_night
        return initial

    def get_success_url(self):
        return reverse_lazy("history_settings")

    def form_valid(self, form):
        valid = True
        if form.cleaned_data.get("old_password").strip().length > 0:
            if self.request.user.check_password(form.cleaned_data.get("old_password")):
                if form.cleaned_data.get("new_password") == form.cleaned_data.get("repeat_password"):
                    try:
                        json = form.authorise(self.request)
                        self.request.user.set_password(form.cleaned_data.get("new_password"))
                        self.request.user.save(broadcast=False, update_fields=["password"])
                        local_user = ZaptecUser.objects.update(
                            email=self.request.user.email,
                            token=json.get(RestResponse.AUTH_BEARER_TOKEN),
                            refresh_token=json.get(RestResponse.AUTH_REFRESH_TOKEN))
                        local_user.save()
                    except RestError:
                        messages.add_message(self.request, messages.INFO, "Nieprawidłowe dane logowania do Zaptec!")
                        valid = False
                else:
                    messages.add_message(self.request, messages.INFO,
                                         "Nowe hasło i jego powtórzenie nie są identyczne!")
                    valid = False
            else:
                messages.add_message(self.request, messages.INFO, "Nieprawidłowe aktualne hasło!")
                valid = False
        if valid is True:
            cost = EnergyCost.objects.update(
                user=self.request.user,
                tariff=form.cleaned_data.get("type"),
                price_day=form.cleaned_data.get("price_day"),
                price_night=form.cleaned_data.get("price_night")
            )
            cost.save()
        return super().form_valid(form) if valid else super().form_invalid(form)
