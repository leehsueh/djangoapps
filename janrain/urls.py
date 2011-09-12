from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$',
	        'siteapps_v1.janrain.views.test'
	    ),
    url(r'^login/$',
        'siteapps_v1.janrain.views.login',
        name='janrain-login'
    ),
    url(r'^logout/$',
        'siteapps_v1.janrain.views.logout',
        name='janrain-logout'
    ),
)