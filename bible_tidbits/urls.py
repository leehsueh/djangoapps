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
    url(r'^(?P<book>(\d-)?[\w-]+)/$',
        'siteapps_v1.bible_tidbits.views.tidbits_by_book',
        name='tidbits-by-book'
    ),
    url(r'^edit/(?P<tidbit_id>\d+)/$',
        'siteapps_v1.bible_tidbits.views.edit',
        name='edit'
    ),
    url(r'^delete/(?P<tidbit_id>\d+)/$',
        'siteapps_v1.bible_tidbits.views.delete',
        name='delete'
    ),
    url(r'^test/$',
        'siteapps_v1.bible_tidbits.views.test_form',
    ),
)
