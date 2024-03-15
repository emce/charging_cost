from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from charging_cost import settings
from history.cost import Cost
from history.managers import ZaptecUserManager


class Charger(models.Model):
    # json.get("Id")
    id = models.CharField(max_length=100, primary_key=True)
    # json.get("Name")
    name = models.CharField(max_length=100)
    # json.get("IsOnline")
    is_online = models.BooleanField()
    # json.get("DeviceId")
    device_id = models.CharField(max_length=20)
    # json.get("OperationMode")
    operating_mode = models.IntegerField(default=0)
    # json.get("CreatedOnDate")
    created = models.DateTimeField()
    # json.get("CircuitId")
    circuit_id = models.CharField(max_length=100)
    # json.get("Active")
    active = models.BooleanField()
    # json.get("Pin")
    pin = models.CharField(max_length=10)
    # json.get("DeviceType")
    device_type = models.IntegerField()
    # json.get("InstallationId")
    installation_id = models.CharField(max_length=100)
    # json.get("InstallationName")
    installation_name = models.CharField(max_length=100)
    # json.get("IsAuthorizationRequired")
    authorization_required = models.BooleanField()


class History(models.Model):
    # json.get("Id")
    id = models.CharField(max_length=200, primary_key=True)
    # json.get("DeviceId")
    device_id = models.CharField(max_length=20)
    # json.get("StartDateTime")
    start = models.DateTimeField()
    # json.get("EndDateTime")
    end = models.DateTimeField()
    # json.get("Energy")
    energy = models.FloatField()
    # json.get("ChargerId")
    charger_id = models.CharField(max_length=100)
    # json.get("DeviceName")
    device_name = models.CharField(max_length=100)


class EnergyCost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tariff = models.IntegerField(choices={
        (Cost.G11.value, Cost.G11.name),
        (Cost.G12.value, Cost.G12.name),
        (Cost.G12W.value, Cost.G12W.name)
    })
    price_day = models.FloatField()
    price_night = models.FloatField()


class ZaptecUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )
    token = models.CharField(max_length=150, blank=True, default="")
    refresh_token = models.CharField(max_length=150, blank=True, default="")

    USERNAME_FIELD = 'email'

    objects = ZaptecUserManager()

    def __str__(self):
        return self.email
