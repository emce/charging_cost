from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import DatabaseError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from charging_cost.rest import RestClient, RestError, RestResponse
from history.models import ZaptecUser


class StartForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def authorise(self, request):
        return RestClient.auth(self.cleaned_data.get("email"), self.cleaned_data.get("password"))


class StartView(FormView):
    template_name = 'start.html'
    form_class = StartForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('history_index'))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("wizard_chargers")

    def form_valid(self, form):
        try:
            json = form.authorise(self.request)
            try:
                local_user = ZaptecUser.objects.update_or_create(
                    username=form.cleaned_data.get("email"),
                    token=json.get(RestResponse.AUTH_BEARER_TOKEN),
                    refresh_token=json.get(RestResponse.AUTH_REFRESH_TOKEN))
                local_user.set_password(form.cleaned_data.get("password"))
                local_user.save()
            except DatabaseError:
                local_user = ZaptecUser.objects.get(email=form.cleaned_data.get("email"))
                local_user.set_password(form.cleaned_data.get("password"))
                local_user.save()
            login_user = authenticate(
                self.request,
                username=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password"))
            if login_user is not None:
                login(self.request, login_user)
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
        except RestError:
            messages.add_message(self.request, messages.INFO, "Nieprawidłowe dane logowania do Zaptec!")
            return super().form_invalid(form)
