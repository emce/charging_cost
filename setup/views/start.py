from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from charging_cost.rest import RestClient, RestError, RestResponse
from charging_cost.session import SessionData
from history.models import ZaptecUser


class StartForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def authorise(self, request):
        return RestClient.auth(self.cleaned_data.get("email"), self.cleaned_data.get("password"))


class StartView(FormView):
    template_name = 'start.html'
    form_class = StartForm

    def get_success_url(self):
        return reverse_lazy("wizard_chargers")

    def get_initial(self):
        if self.request.method == 'GET' and self.request.session.has_key(SessionData.AUTH_BEARER_TOKEN):
            redirect("history_index")

    def form_valid(self, form):
        try:
            json = form.authorise(self.request)
            local_user = ZaptecUser.objects.create(
                email=form.cleaned_data.get("email"),
                token=json.get(RestResponse.AUTH_BEARER_TOKEN),
                refresh_token=json.get(RestResponse.AUTH_REFRESH_TOKEN))
            local_user.set_password(form.cleaned_data.get("password"))
            local_user.save()
            login_user = authenticate(
                self.request,
                username=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password"))
            if login_user is not None:
                login(self.request, login_user)
                local_user.token = json.get(RestResponse.AUTH_BEARER_TOKEN)
                local_user.refresh_token = json.get(RestResponse.AUTH_REFRESH_TOKEN)
                local_user.save()
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
        except RestError:
            messages.add_message(self.request, messages.INFO, "Nieprawidłowe dane logowania do Zaptec!")
            return super().form_invalid(form)
