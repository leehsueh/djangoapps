from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'siteapps_v1.bible_tidbits.views.home',
        name='home'
    ),
)
