from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'siteapps_v1.bible_tidbits.views.home',
        name='home'
    ),
    url(r'^add/$',
        'siteapps_v1.bible_tidbits.views.add',
        name='add'
    ),
    url(r'^edit/(?P<tidbit_id>\d+)/$',
        'siteapps_v1.bible_tidbits.views.edit',
        name='edit'
    ),
)
