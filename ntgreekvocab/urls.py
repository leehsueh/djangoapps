from django.conf.urls.defaults import *
from siteapps_v1.ntgreekvocab.models import SimpleCard

urlpatterns = patterns('',
    # renders template called <modelname>_list.html
    # (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    url(r'^card/all/$',
        'django.views.generic.list_detail.object_list',
        {'queryset':SimpleCard.objects.all().order_by('greek_word')},
        name='cards-all'
    ),
    # renders template called <modelname>_detail.html
    #(r'^entry_g/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
    
    url(r'^$',
        'siteapps_v1.ntgreekvocab.views.home',
        name='home'
    ),
    url(r'^card/random/(?P<card_id>\d+)/$',
        'siteapps_v1.ntgreekvocab.views.card_random_view',
        name='card-random-view'
    ),
    url(r'^card/(?P<card_id>\d+)/$',
        'siteapps_v1.ntgreekvocab.views.card_view',
        name='card-view'
    ),
    url(r'^card/add/$',
        'siteapps_v1.ntgreekvocab.views.card_add',
        name='card-add'
    ),
    url(r'^card/edit/(?P<card_id>\d+)/$',
        'siteapps_v1.ntgreekvocab.views.card_edit',
        name='card-edit'
    ),
    url(r'^card/list/$',
        'siteapps_v1.ntgreekvocab.views.card_list',
        name='cards-list'
    ),
    url(r'^lesson/(?P<lesson_num>(NA|[0-9]{1,2}[ABab]{0,1}))/$',
        'siteapps_v1.ntgreekvocab.views.cards_by_lesson',
        name='lesson'
    ),
    url(r'^card/lookup/$',
        'siteapps_v1.ntgreekvocab.views.card_lookup',
        name='card-lookup'
    ),

    # ajax urls
    url(r'^card_lookup/$',
        'siteapps_v1.ntgreekvocab.views.ajax_card_autocomplete',
        name='ajax-card-autocomplete'
    ),
    url(r'^card/fetch/(?P<card_id>\d+)/$',
        'siteapps_v1.ntgreekvocab.views.ajax_card_fetch',
        name='ajax-card-fetch'
    ),
    url(r'^clearln/$',
        'siteapps_v1.ntgreekvocab.views.ajax_clear_lesson_filters',
        name='ajax-clear-lesson-filters'
    ),
)
