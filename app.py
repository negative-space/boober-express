from cratis import *
from cratis.features import Feature
from cratis_common.bundles import CratisCms
from cratis_common.cratis_sitemap.features import AutoSitemap
from cratis_common.db import Mysql
from cratis_common.inline_edit.features import InlineEdit
from cratis_common.local_server import LocalServerAssets
from cratis_celery.features import Celery
from cratis_common.redis import RedisFull, Redis, RedisCache, RedisSession
from cratis_deploy.features import Uwsgi
from cratis_i18n.features import I18n
from cratis_integrations.sentry import Sentry
from cratis_integrations.sparkpost import Sparkpost
from cratis_profile.features import Profile, ProfileRegistration, AuthFacebook

from boober.features import Boober


class Me(Feature):
    def init(self):
        self.settings.LOGIN_REDIRECT_URL = 'boober.index'

app = App()
app.load(
        AutoSitemap(),

        Mysql('boober', 'root', '123123'),

        CratisCms(langs=('en', 'et', 'ru'
                         # 'fr', 'de', 'sv', 'fi',
                         # 'es', 'lv', 'lt', 'el'
                         ), title='Boober Express'),

        I18n(
            langs=('en', 'et', 'ru'),
            fallback_translations=True,
            django_url_middleware=True
        ),

        InlineEdit(app_names=['boober', 'cratis_i18n']),

        Boober(),

        Profile(),
        ProfileRegistration(),

        Sparkpost(key='ba649d7d134ec5e692d710a2e596e3033efac335'),
    )

with app.conf(Dev):
    app.load(
        # DebugToolbar(),

        LocalServerAssets(),
    )


with app.conf(Prod):
    app.load(
        Mysql('app', 'root', '123123', 'mysql'),

        Celery(hostname='redis'),

        Redis(host='redis'),
        RedisCache(host='redis'),
        RedisSession(host='redis'),

        # AuthFacebook(),

        Uwsgi(),

        Sentry(dsn='https://97871b9c00624eeeabecb15ca4e7dacf:a6503477fa2c460bbfacd3ca7abfd5c9@sentry.io/893831')

    )


Dev.ALLOWED_HOSTS = ['*']
Prod.ALLOWED_HOSTS = ['*']
Prod.SECRET_KEY = 'lqYVdvxKxjkjqsHbfysTBryWha0Vb9gc'
Prod.TIME_ZONE = 'Europe/Tallinn'
Prod.LOGIN_REDIRECT_URL = '/'


Dev.DEFAULT_FROM_EMAIL = 'boobmaster@boober.express'
Prod.DEFAULT_FROM_EMAIL = 'boobmaster@boober.express'

app.run(locals())
