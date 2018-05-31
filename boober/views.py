from boober.models import Driver, Ride, Proposal, ProposalPickup, RideFeedback, DriverProposalCancel, Client, ProposalAccept, RideCancelation
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from boober.models import Driver, Ride, Client
from cratis_i18n.trans_utils import _


if '_' not in locals():
    def _(s): return s


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ['id', 'location_lat', 'location_lon']

    def create(self, validated_data):

        item = Driver.objects.create(
            user=self.context.get('request').user, **validated_data)

        return item


class DriverViewSet(ModelViewSet):
    """
    Driver API
    """

    filter_fields = ['id', 'location_lat', 'location_lon']
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return Driver.objects.all().filter(user=self.request.user)


class Ride_InlineDriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = ['id', 'location_lat', 'location_lon']


class RideSerializer(serializers.ModelSerializer):

    driver = Ride_InlineDriverSerializer(many=False, read_only=False)

    class Meta:
        model = Ride
        fields = ['id', 'driver', 'status']


class RideViewSet(ReadOnlyModelViewSet):
    """
    Ride API
    """

    filter_fields = ['id', 'driver', 'status']
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return Ride.objects.filter(client__user=self.request.user)


def cached(func, suffix='data'):
    def _wrap(self, *args, **kwargs):
        if hasattr(self, '_' + suffix):
            return getattr(self, '_' + suffix)
        data = func(self, *args, **kwargs)
        setattr(self, '_' + suffix, data)
        return data
    return _wrap


class _Data(object):
    def __init__(self, data=None):
        self.__dict__.update(data or {})

    def __add__(self, data):
        return _Data({**self.__dict__, **data})


class _View(object):
    def get_data(self, inherited):
        return _Data()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**self.kwargs)
        return {**data, **self.get_data().__dict__}


class MapView(_View, TemplateView):

    def get_template_names(self):
        return ["boober/map.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        return data + {'url': url}


class BaseView(_View, TemplateView):

    def get_template_names(self):
        return ["boober/base.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        data.menu_main = {
            'index': {'label': _('Home'), 'link': reverse_lazy('boober.index'), 'icon': "home"},
            'client': {'label': _('Ride'), 'link': reverse_lazy('boober.client_start')},
            'driver': {'label': _('Drive'), 'link': reverse_lazy('boober.driver_start')},
        }

        return data + {'url': url}


class IndexView(BaseView):

    def activate_main_menu(self, *args, **kwargs):
        self.get_data().menu_main['index']['active'] = True

    def get_template_names(self):
        return ["boober/index.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        self.activate_main_menu()

        return data + {'url': url}


class ThankyouView(BaseView):

    def get_template_names(self):
        return ["boober/thankyou.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        return data + {'url': url}


class DriverThankyouView(BaseView):

    def get_template_names(self):
        return ["boober/driver_thankyou.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        ride = Ride.objects.get(pk=url.ride)
        data.ride = ride

        return data + {'url': url, 'ride': ride}


@method_decorator(login_required, name='dispatch')
class UserBaseView(BaseView):

    def get_template_names(self):
        return ["boober/user_base.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        return data + {'url': url}


@method_decorator(login_required, name='dispatch')
class DriverZoneView(UpdateView, UserBaseView):
    pk_url_kwarg = 'pk'
    model = Driver
    context_object_name = 'item'
    fields = ['name', 'age', 'car_model', 'phone', 'own_photo', 'car_photo']

    def get_success_url(self, *args, **kwargs):
        request = self.request

        return self.request.get_full_path()

    def get_queryset(self, *args, **kwargs):
        request = self.request

        return Driver.objects.filter(user=request.user)

    def get(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return super().get(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return super().post(self.request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return self.object

    def get_template_names(self):
        return ["boober/driver_zone.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        profile = Driver.objects.get_or_create(user=request.user)[0]
        data.profile = profile

        return data + {'url': url, 'profile': profile}


@method_decorator(login_required, name='dispatch')
class DriverStartView(UpdateView, UserBaseView):
    pk_url_kwarg = 'pk'
    model = Driver
    context_object_name = 'item'
    fields = ['name', 'age', 'car_model', 'phone', 'own_photo', 'car_photo']

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('boober.open_rides_list')

    def get_queryset(self, *args, **kwargs):
        request = self.request

        return Driver.objects.filter(user=request.user)

    def get(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return super().get(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return super().post(self.request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return self.object

    def activate_main_menu(self, *args, **kwargs):
        self.get_data().menu_main['driver']['active'] = True

    def get_template_names(self):
        return ["boober/driver_start.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        profile = Driver.objects.get_or_create(user=request.user)[0]
        data.profile = profile

        self.activate_main_menu()

        return data + {'url': url, 'profile': profile}


@method_decorator(login_required, name='dispatch')
class RideBaseView(UserBaseView):

    def get_template_names(self):
        return ["boober/ride_base.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        try:
            ride = Ride.objects.get(pk=url.pk)
            data.ride = ride
        except ObjectDoesNotExist:
            raise Http404

        return data + {'url': url, 'ride': ride}


@method_decorator(login_required, name='dispatch')
class OpenRidesListView(UserBaseView):

    def get_template_names(self):
        return ["boober/open_rides_list.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        rides = Ride.objects.filter(status='waiting_proposals')
        data.rides = rides
        profile = Driver.objects.get_or_create(user=request.user)[0]
        data.profile = profile

        return data + {'url': url, 'rides': rides, 'profile': profile}


@method_decorator(login_required, name='dispatch')
class RideDetailView(CreateView, RideBaseView):
    pk_url_kwarg = 'pk'
    model = Proposal
    context_object_name = 'item'
    fields = ['comment']

    def get_success_url(self, *args, **kwargs):
        url = type('url', (object,), self.kwargs)

        return reverse_lazy('boober.driver_waiting', kwargs={'pk': url.pk, 'proposal': self.object.pk})

    def get_queryset(self, *args, **kwargs):
        data = self.get_data()

        return Proposal.objects.filter(driver=data.driver, ride=data.ride)

    def get(self, *args, **kwargs):
        self.object = None
        return super().get(self.request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        data = self.get_data()

        self.object = Proposal(driver=data.driver, ride=data.ride)
        return super().get_initial()

    def get_template_names(self):
        return ["boober/ride_detail.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        driver = Driver.objects.get(user=request.user)
        data.driver = driver

        return data + {'url': url, 'driver': driver}


@method_decorator(login_required, name='dispatch')
class DriverWaitingView(CreateView, RideBaseView):
    pk_url_kwarg = 'pk'
    model = ProposalPickup
    context_object_name = 'item'
    fields = ['consent']

    def get_success_url(self, *args, **kwargs):
        url = type('url', (object,), self.kwargs)

        return reverse_lazy('boober.driver_ride', kwargs={'pk': url.pk})

    def get_queryset(self, *args, **kwargs):
        data = self.get_data()

        return ProposalPickup.objects.filter(proposal=data.proposal)

    def get(self, *args, **kwargs):
        self.object = None
        return super().get(self.request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        data = self.get_data()

        self.object = ProposalPickup(proposal=data.proposal)
        return super().get_initial()

    def get_template_names(self):
        return ["boober/driver_waiting.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        driver = Driver.objects.get(user=request.user)
        data.driver = driver
        profile = Driver.objects.get_or_create(user=request.user)[0]
        data.profile = profile
        ride = Ride.objects.get(pk=url.pk)
        data.ride = ride
        proposal = Proposal.objects.get(pk=url.proposal)
        data.proposal = proposal

        return data + {'url': url, 'driver': driver, 'profile': profile, 'ride': ride, 'proposal': proposal}


@method_decorator(login_required, name='dispatch')
class DriverRideView(RideBaseView):

    def get_template_names(self):
        return ["boober/driver_ride.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        ride = Ride.objects.get(pk=url.pk)
        data.ride = ride

        return data + {'url': url, 'ride': ride}


@method_decorator(login_required, name='dispatch')
class DriverRideFeedbackView(CreateView, RideBaseView):
    pk_url_kwarg = 'pk'
    model = RideFeedback
    context_object_name = 'item'
    fields = ['paid', 'feedback', 'picture']

    def get_success_url(self, *args, **kwargs):
        data = self.get_data()

        return reverse_lazy('boober.driver_thankyou', kwargs={'ride': data.ride.pk})

    def get_queryset(self, *args, **kwargs):
        data = self.get_data()

        return RideFeedback.objects.filter(ride=data.ride)

    def get(self, *args, **kwargs):
        self.object = None
        return super().get(self.request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        data = self.get_data()

        self.object = RideFeedback(ride=data.ride)
        return super().get_initial()

    def get_template_names(self):
        return ["boober/driver_ride_feedback.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        ride = Ride.objects.get(pk=url.pk)
        data.ride = ride

        return data + {'url': url, 'ride': ride}


@method_decorator(login_required, name='dispatch')
class DriverProposalCancelView(CreateView, RideBaseView):
    pk_url_kwarg = 'pk'
    model = DriverProposalCancel
    context_object_name = 'item'
    fields = ['reason']

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('boober.open_rides_list')

    def get_queryset(self, *args, **kwargs):
        data = self.get_data()

        return DriverProposalCancel.objects.filter(proposal=data.proposal)

    def get(self, *args, **kwargs):
        self.object = None
        return super().get(self.request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        data = self.get_data()

        self.object = DriverProposalCancel(proposal=data.proposal)
        return super().get_initial()

    def get_template_names(self):
        return ["boober/driver_proposal_cancel.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        try:
            proposal = Proposal.objects.get(pk=url.proposal)
            data.proposal = proposal
        except ObjectDoesNotExist:
            raise Http404

        return data + {'url': url, 'proposal': proposal}


@method_decorator(login_required, name='dispatch')
class ClientZoneView(UpdateView, UserBaseView):
    pk_url_kwarg = 'pk'
    model = Client
    context_object_name = 'item'
    fields = ['name', 'age', 'own_photo', 'phone', 'boobs_size']

    def get_success_url(self, *args, **kwargs):
        request = self.request

        return self.request.get_full_path()

    def get_queryset(self, *args, **kwargs):
        request = self.request

        return Client.objects.filter(user=request.user)

    def get(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return super().get(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return super().post(self.request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return self.object

    def get_template_names(self):
        return ["boober/client_zone.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        profile = Client.objects.get_or_create(user=request.user)[0]
        data.profile = profile
        last_rides = Ride.objects.filter(client=profile)[:10]
        data.last_rides = last_rides

        return data + {'url': url, 'profile': profile, 'last_rides': last_rides}


@method_decorator(login_required, name='dispatch')
class ClientStartView(UpdateView, UserBaseView):
    pk_url_kwarg = 'pk'
    model = Client
    context_object_name = 'item'
    fields = ['name', 'age', 'own_photo', 'phone', 'boobs_size']

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('boober.client_ordering')

    def get_queryset(self, *args, **kwargs):
        request = self.request

        return Client.objects.filter(user=request.user)

    def get(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return super().get(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return super().post(self.request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        data = self.get_data()

        self.object = data.profile
        return self.object

    def activate_main_menu(self, *args, **kwargs):
        self.get_data().menu_main['client']['active'] = True

    def get_template_names(self):
        return ["boober/client_start.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        profile = Client.objects.get_or_create(user=request.user)[0]
        data.profile = profile

        self.activate_main_menu()

        return data + {'url': url, 'profile': profile}


@method_decorator(login_required, name='dispatch')
class ClientOrderingView(CreateView, UserBaseView):
    pk_url_kwarg = 'pk'
    model = Ride
    context_object_name = 'item'
    fields = ['pickup_point_lat', 'pickup_point_lon', 'pickup_address']

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('boober.client_waiting', kwargs={'pk': self.object.pk})

    def get_queryset(self, *args, **kwargs):
        data = self.get_data()

        return Ride.objects.filter(client=data.profile, status='waiting_proposals')

    def get(self, *args, **kwargs):
        self.object = None
        return super().get(self.request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        data = self.get_data()

        self.object = Ride(client=data.profile, status='waiting_proposals')
        return super().get_initial()

    def get_template_names(self):
        return ["boober/client_ordering.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        profile = Client.objects.get(user=request.user)
        data.profile = profile

        return data + {'url': url, 'profile': profile}


@method_decorator(login_required, name='dispatch')
class ClientWaitingView(RideBaseView):

    def get_template_names(self):
        return ["boober/client_waiting.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        profile = Client.objects.get(user=request.user)
        data.profile = profile
        proposals = data.ride.proposals.filter(cancelled=False)
        data.proposals = proposals

        return data + {'url': url, 'profile': profile, 'proposals': proposals}


@method_decorator(login_required, name='dispatch')
class ClientProposalAcceptView(CreateView, UserBaseView):
    pk_url_kwarg = 'pk'
    model = ProposalAccept
    context_object_name = 'item'
    fields = ['consent']

    def get_success_url(self, *args, **kwargs):
        url = type('url', (object,), self.kwargs)

        return reverse_lazy('boober.ride_waiting', kwargs={'pk': url.pk, 'proposal': url.proposal})

    def get_queryset(self, *args, **kwargs):
        data = self.get_data()

        return ProposalAccept.objects.filter(proposal=data.proposal)

    def get(self, *args, **kwargs):
        self.object = None
        return super().get(self.request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        data = self.get_data()

        self.object = ProposalAccept(proposal=data.proposal)
        return super().get_initial()

    def get_template_names(self):
        return ["boober/client_proposal_accept.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        request = self.request
        url = type('url', (object,), self.kwargs)

        profile = Client.objects.get(user=request.user)
        data.profile = profile
        proposal = Proposal.objects.get(pk=url.proposal)
        data.proposal = proposal
        ride = proposal.ride
        data.ride = ride

        return data + {'url': url, 'profile': profile, 'proposal': proposal, 'ride': ride}


@method_decorator(login_required, name='dispatch')
class ClientCancelView(CreateView, RideBaseView):
    pk_url_kwarg = 'pk'
    model = RideCancelation
    context_object_name = 'item'
    fields = ['reason']

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('boober.client_start')

    def get_queryset(self, *args, **kwargs):
        data = self.get_data()

        return RideCancelation.objects.filter(ride=data.ride)

    def get(self, *args, **kwargs):
        self.object = None
        return super().get(self.request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        data = self.get_data()

        self.object = RideCancelation(ride=data.ride)
        return super().get_initial()

    def get_template_names(self):
        return ["boober/client_cancel.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        return data + {'url': url}


@method_decorator(login_required, name='dispatch')
class RideWaitingView(RideBaseView):

    def get_template_names(self):
        return ["boober/ride_waiting.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        proposal = Proposal.objects.get(pk=url.proposal)
        data.proposal = proposal

        return data + {'url': url, 'proposal': proposal}


@method_decorator(login_required, name='dispatch')
class ProposedDriversView(RideBaseView):

    def get_template_names(self):
        return ["boober/proposed_drivers.html"]

    @cached
    def get_data(self, inherited=False):
        data = super().get_data(inherited=True)
        url = type('url', (object,), self.kwargs)

        return data + {'url': url}
