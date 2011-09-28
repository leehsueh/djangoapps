from django.conf.urls.defaults import *

urlpatterns = patterns('',

    url(r'^list/$',
        'siteapps_v1.google_docs_reftagger.views.get_folder_list',
        name='folder-list'
    ),
    url(r'^folder/(?P<resource_id>[a-z]+:[0-9a-zA-Z_\-]+)/$',
        'siteapps_v1.google_docs_reftagger.views.get_folder_contents',
        name='folder-docs'
    ),
    url(r'^doc/(?P<resource_id>[a-z]+:[0-9a-zA-Z_\-]+)/$',
        'siteapps_v1.google_docs_reftagger.views.get_doc_content',
        name='doc'
    ),
)
