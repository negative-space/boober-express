
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from cratis_i18n.trans_utils import _


if '_' not in locals():
    def _(s): return s


class Driver(models.Model):
    """
    Driver
    """

    user = models.ForeignKey("cratis_profile.User", verbose_name=_(
        'User'), null=True, blank=True, related_name='drivers', on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    name = models.CharField(verbose_name=_(
        'Name'), null=True, blank=False, max_length=100)
    age = models.IntegerField(verbose_name=_('Age'), null=True, blank=False)
    car_model = models.CharField(verbose_name=_(
        'Car model'), null=True, blank=False, max_length=100)
    phone = models.CharField(verbose_name=_(
        'Phone'), null=True, blank=False, max_length=100)
    own_photo = models.ImageField(verbose_name=_(
        'Selfie'), null=True, blank=True, upload_to='image_upload/driver/own_photo')
    car_photo = models.ImageField(verbose_name=_(
        'Car photo'), null=True, blank=True, upload_to='image_upload/driver/car_photo')
    location_lat = models.CharField(verbose_name=_(
        'Location lat'), null=True, blank=True, max_length=100, default='')
    location_lon = models.CharField(verbose_name=_(
        'Location lon'), null=True, blank=True, max_length=100, default='')

    def __str__(self):
        return str(self.name) or "Driver {}".format(self.id)

    class Meta:
        verbose_name = _("Driver")


class Client(models.Model):
    """
    Client
    """

    user = models.ForeignKey("cratis_profile.User", verbose_name=_(
        'User'), null=True, blank=True, related_name='clients', on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    name = models.CharField(verbose_name=_(
        'Name'), null=True, blank=False, max_length=100)
    age = models.IntegerField(verbose_name=_('Age'), null=True, blank=False)
    own_photo = models.ImageField(verbose_name=_(
        'Selfie'), null=True, blank=False, upload_to='image_upload/client/own_photo')
    phone = models.CharField(verbose_name=_(
        'Phone'), null=True, blank=False, max_length=100)
    location_lat = models.CharField(verbose_name=_(
        'Location lat'), null=True, blank=True, max_length=100, default='')
    location_lon = models.CharField(verbose_name=_(
        'Location lon'), null=True, blank=True, max_length=100, default='')
    boobs_size = models.IntegerField(
        verbose_name=_('Boobs size'), null=True, blank=False)

    def __str__(self):
        return str(self.name) or "Client {}".format(self.id)

    class Meta:
        verbose_name = _("Client")


class Ride(models.Model):
    """
    Ride
    """

    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    client = models.ForeignKey("Client", verbose_name=_(
        'Client'), null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    driver = models.ForeignKey("Driver", verbose_name=_(
        'Driver'), null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    pickup_point_lat = models.CharField(verbose_name=_(
        'Pickup point lat'), null=True, blank=True, max_length=100, default='')
    pickup_point_lon = models.CharField(verbose_name=_(
        'Pickup point lon'), null=True, blank=True, max_length=100, default='')
    pickup_address = models.CharField(verbose_name=_(
        'Pickup address'), null=True, blank=True, max_length=255, default='')
    start_time = models.DateTimeField(
        verbose_name=_('Start time'), null=True, blank=True)
    status = models.CharField(verbose_name=_('Status'), null=True, blank=True, max_length=17, default='', choices=(
        ('waiting_proposals', 'waiting_proposals'), ('client_accepted', 'client_accepted'), ('ride', 'ride'), ('canceled', 'canceled'), ('done', 'done')))
    pickup_time = models.DateTimeField(
        verbose_name=_('Pickup time'), null=True, blank=True)
    end_time = models.DateTimeField(
        verbose_name=_('End time'), null=True, blank=True)
    paid = models.BooleanField(verbose_name=_(
        'I have seen the boobs'), blank=True, default=False)
    selected_proposal = models.ForeignKey("Proposal", verbose_name=_(
        'Selected proposal'), null=True, blank=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        return "{me.client} ({me.status})".format(me=self)

    class Meta:
        verbose_name = _("Ride")


class RideCancelation(models.Model):
    """
    RideCancelation
    """

    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    ride = models.OneToOneField("Ride", verbose_name=_(
        'Ride'), null=True, blank=True, related_name='cancelation', on_delete=models.CASCADE)
    reason = models.TextField(verbose_name=_(
        'Reason'), null=True, blank=True, default='')

    class Meta:
        verbose_name = _("Ride cancelation")


@receiver(post_save, sender=RideCancelation)
def ride_cancelation_post_save_callback(sender, instance, **kwargs):
    args = type('args', (object,), kwargs)
    instance.ride.status = 'canceled'
    instance.ride.save()


class Proposal(models.Model):
    """
    Proposal
    """

    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    driver = models.ForeignKey("Driver", verbose_name=_(
        'Driver'), null=True, blank=True, related_name='my_proposals', on_delete=models.CASCADE)
    ride = models.ForeignKey("Ride", verbose_name=_(
        'Ride'), null=True, blank=True, related_name='proposals', on_delete=models.CASCADE)
    accepted = models.BooleanField(verbose_name=_(
        'Accepted'), blank=True, default=False)
    distance = models.IntegerField(
        verbose_name=_('Distance'), null=True, blank=True)
    comment = models.CharField(verbose_name=_(
        'Add notes that will be visible for client, or just say "Hello!"'), null=True, blank=True, max_length=100, default='')
    cancelled = models.BooleanField(verbose_name=_(
        'Cancelled'), blank=True, default=False)

    class Meta:
        verbose_name = _("Proposal")


class DriverProposalCancel(models.Model):
    """
    DriverProposalCancel
    """

    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    proposal = models.ForeignKey("Proposal", verbose_name=_(
        'Proposal'), null=True, blank=True, related_name='proposal_status', on_delete=models.CASCADE)
    reason = models.TextField(verbose_name=_(
        'Reason'), null=True, blank=True, default='')

    class Meta:
        verbose_name = _("Driver proposal cancel")


@receiver(post_save, sender=DriverProposalCancel)
def driver_proposal_cancel_post_save_callback(sender, instance, **kwargs):
    args = type('args', (object,), kwargs)
    instance.proposal.ride.status = 'waiting_proposals'
    instance.proposal.cancelled = True
    instance.proposal.save()
    instance.proposal.ride.save()


class ProposalAccept(models.Model):
    """
    ProposalAccept
    """

    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    proposal = models.ForeignKey("Proposal", verbose_name=_(
        'Proposal'), null=True, blank=True, related_name='accept', on_delete=models.CASCADE)
    consent = models.BooleanField(verbose_name=_(
        'I confirm I am at least 18 years old, and I will need to show naked boobs to the driver after the ride.'), blank=False, default=False)

    class Meta:
        verbose_name = _("Proposal accept")


@receiver(post_save, sender=ProposalAccept)
def proposal_accept_post_save_callback(sender, instance, **kwargs):
    args = type('args', (object,), kwargs)
    instance.proposal.ride.status = 'client_accepted'
    instance.proposal.ride.selected_proposal = instance.proposal
    instance.proposal.ride.driver = instance.proposal.driver
    instance.proposal.ride.save()

    instance.proposal.accepted = True
    instance.proposal.save()


class ProposalPickup(models.Model):
    """
    ProposalPickup
    """

    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    proposal = models.ForeignKey("Proposal", verbose_name=_(
        'Proposal'), null=True, blank=True, related_name='pickup', on_delete=models.CASCADE)
    consent = models.BooleanField(verbose_name=_(
        "I confirm I am at least 18 years old, and I'm not against to see naked boobs after the ride."), blank=False, default=False)

    class Meta:
        verbose_name = _("Proposal pickup")


@receiver(post_save, sender=ProposalPickup)
def proposal_pickup_post_save_callback(sender, instance, **kwargs):
    args = type('args', (object,), kwargs)
    instance.proposal.ride.status = 'ride'
    instance.proposal.ride.save()


class RideFeedback(models.Model):
    """
    RideFeedback
    """

    date_created = models.DateTimeField(verbose_name=_(
        'Date created'), null=True, blank=True, auto_now_add=True)
    ride = models.OneToOneField("Ride", verbose_name=_(
        'Ride'), null=True, blank=True, related_name='feedback', on_delete=models.CASCADE)
    paid = models.BooleanField(verbose_name=_(
        'I have seen the boobs!'), blank=True, default=False)
    feedback = models.TextField(verbose_name=_(
        'Write couple words to your client'), null=True, blank=True, default='')
    picture = models.ImageField(verbose_name=_('Proof of successful payment (ask first, no face on picture!)'),
                                null=True, blank=True, upload_to='image_upload/ride_feedback/picture')

    class Meta:
        verbose_name = _("Ride feedback")


@receiver(post_save, sender=RideFeedback)
def ride_feedback_post_save_callback(sender, instance, **kwargs):
    args = type('args', (object,), kwargs)
    instance.ride.paid = instance.paid
    instance.ride.status = 'done'
    instance.ride.save()
