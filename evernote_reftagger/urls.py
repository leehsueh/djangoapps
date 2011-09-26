from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'siteapps_v1.evernote_reftagger.views.list_notes',
        name='list-notes'
    ),
    url(r'^pub/(?P<username>[a-z0-9]([a-z0-9_-]{0,62}[a-z0-9])?)/(?P<uri>[a-zA-Z0-9.~_+-]{1,255})/$',
        'siteapps_v1.evernote_reftagger.views.public_notebook',
        name='public-notebook'
    ),
    url(r'^pub/(?P<username>[a-z0-9]([a-z0-9_-]{0,62}[a-z0-9])?)/(?P<uri>[a-zA-Z0-9.~_+-]{1,255})/(?P<note_guid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        'siteapps_v1.evernote_reftagger.views.fetch_public_note',
        name='public-note'
    ),
)
