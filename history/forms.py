from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from history.models import ZaptecUser


class ZaptecUserCreationForm(UserCreationForm):
    class Meta:
        model = ZaptecUser
        fields = ('email',)


class ZaptecUserChangeForm(UserChangeForm):
    class Meta:
        model = ZaptecUser
        fields = ('email',)
