from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^$', 'siteapps_v1.views.hub'),
    (r'^', include('siteapps_v1.bibledb.urls', namespace='bibledb', app_name='bibledb')),
    
    # NT greek app
    (r'^ntgreek/', include('siteapps_v1.ntgreekvocab.urls', namespace='ntgreekvocab', app_name='ntgreekvocab')),

    # Bible tidbits app
    (r'^tidbits/', include('siteapps_v1.bible_tidbits.urls', namespace='tidbits', app_name='bible_tidbits')),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^bibledb/', include('siteapps_v1.bibledb.urls')),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # user accounts
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'siteapps_v1.bibledb.views.logout_view', name='logout'),
    url(r'^accounts/pc/$', 'django.contrib.auth.views.password_change', name='passwd-change'),
    url(r'^accounts/pc/done/$', 'django.contrib.auth.views.password_change_done', name='passwd-change-done'),

    # contactable ajax url; should have POST parameters
    url(r'^contact/$', 'siteapps_v1.views.ajax_contactable', name='ajax-contactable'),

    url(r'^env_info/$', 'siteapps_v1.views.env_info', name='env-info'),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',  
         {'document_root':     settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',  
         {'document_root':     settings.MEDIA_ROOT}),
    )
