from cratis.features import Feature, require

from cratis_admin.features import AdminArea


@require(
    AdminArea(),


)
class Boober(Feature):

    def init(self):
        self.append_apps(['boober'])

        with self.use(AdminArea) as admin:
            admin.add_menu({'label': 'boober', 'models': (
                'boober.Driver',
                'boober.Client',
                'boober.Ride',
                'boober.RideCancelation',
                'boober.Proposal',
                'boober.DriverProposalCancel',
                'boober.ProposalAccept',
                'boober.ProposalPickup',
                'boober.RideFeedback',
            )})

    def configure_urls(self, urls):
        from django.conf.urls import url, include
        from django.conf.urls.i18n import i18n_patterns
        urls += tuple(i18n_patterns(
            url(r'^', include('boober.urls_i18n')),
        ))

        urls += tuple(i18n_patterns(
            url(r'^api-auth/', include('rest_framework.urls',
                                       namespace='rest_framework')),
            url(r'^api/boober/', include('boober.urls_rest')),
        ))
