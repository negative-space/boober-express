from .views import MapView, IndexView, ThankyouView, DriverThankyouView, DriverZoneView, DriverStartView, OpenRidesListView, RideDetailView, DriverWaitingView, DriverRideView, DriverRideFeedbackView, DriverProposalCancelView, ClientZoneView, ClientStartView, ClientOrderingView, ClientWaitingView, ClientProposalAcceptView, ClientCancelView, RideWaitingView, ProposedDriversView
from django.conf.urls import url

urlpatterns = (
    url(r'^map$', MapView.as_view(), name='boober.map'),

    url(r'^$', IndexView.as_view(), name='boober.index'),

    url(r'^thankyou/$', ThankyouView.as_view(), name='boober.thankyou'),

    url(r'^driver_thankyou/(?P<ride>[^\/]+)/$',
        DriverThankyouView.as_view(), name='boober.driver_thankyou'),

    url(r'^driver/$', DriverZoneView.as_view(), name='boober.driver_zone'),

    url(r'^driver/start$', DriverStartView.as_view(), name='boober.driver_start'),

    url(r'^driver/orders/$', OpenRidesListView.as_view(),
        name='boober.open_rides_list'),

    url(r'^driver/order/(?P<pk>[^\/]+)$',
        RideDetailView.as_view(), name='boober.ride_detail'),

    url(r'^driver/order/(?P<pk>[^\/]+)/wait/(?P<proposal>[^\/]+)/$',
        DriverWaitingView.as_view(), name='boober.driver_waiting'),

    url(r'^driver/order/(?P<pk>[^\/]+)/ride/$',
        DriverRideView.as_view(), name='boober.driver_ride'),

    url(r'^driver/order/(?P<pk>[^\/]+)/feedback/$',
        DriverRideFeedbackView.as_view(), name='boober.driver_ride_feedback'),

    url(r'^driver/order/(?P<pk>[^\/]+)/cancel/(?P<proposal>[^\/]+)/$',
        DriverProposalCancelView.as_view(), name='boober.driver_proposal_cancel'),

    url(r'^profile/$', ClientZoneView.as_view(), name='boober.client_zone'),

    url(r'^girl/start$', ClientStartView.as_view(), name='boober.client_start'),

    url(r'^profile/new/order/$', ClientOrderingView.as_view(),
        name='boober.client_ordering'),

    url(r'^boobing/(?P<pk>[^\/]+)$',
        ClientWaitingView.as_view(), name='boober.client_waiting'),

    url(r'^boobing/(?P<pk>[^\/]+)/accept/(?P<proposal>[^\/]+)$',
        ClientProposalAcceptView.as_view(), name='boober.client_proposal_accept'),

    url(r'^boobing/(?P<pk>[^\/]+)/cancel$',
        ClientCancelView.as_view(), name='boober.client_cancel'),

    url(r'^boobing/(?P<pk>[^\/]+)/wait/(?P<proposal>[^\/]+)$',
        RideWaitingView.as_view(), name='boober.ride_waiting'),

    url(r'^boobing/(?P<pk>[^\/]+)/drivers/$',
        ProposedDriversView.as_view(), name='boober.proposed_drivers'),
)
