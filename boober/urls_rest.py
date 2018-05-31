from .views import DriverViewSet, RideViewSet
from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'driver', DriverViewSet, r'driver')
router.register(r'ride', RideViewSet, r'ride')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),

]
