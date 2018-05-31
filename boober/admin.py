
from boober.models import Driver, Client, Ride, Proposal, ProposalAccept, ProposalPickup
from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django_select2.forms import Select2Widget


class DriverModelForm(forms.ModelForm):
    class Meta:
        model = Driver
        exclude = ()
        widgets = {
            'user': Select2Widget,
        }


class DriverAdmin(ModelAdmin):
    """
    Driver Admin
    """

    form = DriverModelForm

    list_display = ['user', 'date_created', 'name', 'age', 'car_model',
                    'phone', 'own_photo', 'car_photo', 'location_lat', 'location_lon']


admin.site.register(Driver, DriverAdmin)


class ClientModelForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ()
        widgets = {
            'user': Select2Widget,
        }


class ClientAdmin(ModelAdmin):
    """
    Client Admin
    """

    form = ClientModelForm


admin.site.register(Client, ClientAdmin)


class RideModelForm(forms.ModelForm):
    class Meta:
        model = Ride
        exclude = ()
        widgets = {
            'client': Select2Widget, 'driver': Select2Widget, 'selected_proposal': Select2Widget,
        }


class RideAdmin(ModelAdmin):
    """
    Ride Admin
    """

    form = RideModelForm

    list_display = ['date_created', 'status']


admin.site.register(Ride, RideAdmin)


class ProposalModelForm(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ()
        widgets = {
            'driver': Select2Widget, 'ride': Select2Widget,
        }


class ProposalAdmin(ModelAdmin):
    """
    Proposal Admin
    """

    form = ProposalModelForm


admin.site.register(Proposal, ProposalAdmin)


class ProposalAcceptModelForm(forms.ModelForm):
    class Meta:
        model = ProposalAccept
        exclude = ()
        widgets = {
            'proposal': Select2Widget,
        }


class ProposalAcceptAdmin(ModelAdmin):
    """
    ProposalAccept Admin
    """

    form = ProposalAcceptModelForm


admin.site.register(ProposalAccept, ProposalAcceptAdmin)


class ProposalPickupModelForm(forms.ModelForm):
    class Meta:
        model = ProposalPickup
        exclude = ()
        widgets = {
            'proposal': Select2Widget,
        }


class ProposalPickupAdmin(ModelAdmin):
    """
    ProposalPickup Admin
    """

    form = ProposalPickupModelForm


admin.site.register(ProposalPickup, ProposalPickupAdmin)
