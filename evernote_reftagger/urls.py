from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # renders template called <modelname>_list.html
    # (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    url(r'^$',
        'siteapps_v1.evernote_reftagger.views.test',
    ),
    url(r'^callback/$',
        'siteapps_v1.evernote_reftagger.views.oauth_callback',
    ),
)
