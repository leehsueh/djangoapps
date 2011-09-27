from django.conf.urls.defaults import *
from siteapps_v1.bibledb.feeds2 import RecentEntriesFeed, RecentEntriesAtomFeed, RecentCommentsFeed, RecentCommentsAtomFeed

urlpatterns = patterns('',
    # clear session (for testing/debug/development only
    (r'^clr/$', 'siteapps_v1.bibledb.views.clear_session'),
    
    url(r'^$', 'siteapps_v1.bibledb.views.home', name='home'),
    url(r'^faq/$', 'siteapps_v1.bibledb.views.faq', name='faq'),
    
    # entry related urls
    url(r'^entry/$', 'siteapps_v1.bibledb.views.display_entries', name='entries-browse'),
    url(r'^entry/all/$', 'siteapps_v1.bibledb.views.display_entries', {'type':'all'}, name='entries-all'),
    url(r'^entry/user/$', 'siteapps_v1.bibledb.views.display_entries', {'type':'username'}, name='users'),
    url(r'^entry/user/(?P<slug>(([a-z0-9=]+-?)+))/$', 'siteapps_v1.bibledb.views.display_entries', {'type':'username'}, name='entries-username'),
    url(r'^entry/(?P<entry_id>\d+)/$', 'siteapps_v1.bibledb.views.display_entry', name='entry-view'),
    # url(r'^entry/(?P<entry_id>\d+)/edit/$', 'siteapps_v1.bibledb.views.edit_entry', name='entry-edit'),
    # url(r'^entry/(?P<entry_id>\d+)/delete/$', 'siteapps_v1.bibledb.views.remove_entry', name='entry-remove'),
    url(r'^entry/(?P<bookname>[0-9]?(-?[a-zA-Z]+)+)/$', 'siteapps_v1.bibledb.views.display_entries', {'type':'passage'}, name='entries-book'),
    url(r'^entry/(?P<bookname>[0-9]?(-?[a-zA-Z]+)+)/(?P<chpnum>[0-9]+)/$', 'siteapps_v1.bibledb.views.display_entries', {'type':'passage'}, name='entries-chapter'),
    url(r'^category/$', 'siteapps_v1.bibledb.views.display_entries',{'type':'category',}, name='categories'),
    url(r'^category/(?P<slug>(([a-z0-9]+-?)+))/$', 'siteapps_v1.bibledb.views.display_entries',{'type':'category',}, name='entries-cat'),
    url(r'^tag/$', 'siteapps_v1.bibledb.views.display_entries',{'type':'tag',}, name='tags'),
    url(r'^tag/(?P<slug>(([a-z0-9]+-?)+))/$', 'siteapps_v1.bibledb.views.display_entries',{'type':'tag',}, name='entries-tag'),
    
    # view bible related urls
    url(r'^bible/$', 'siteapps_v1.bibledb.views.browse_kjv', name='browse-kjv'),
    url(r'^bible/(?P<bookname>[0-9]?(-?[a-zA-Z]+)+)/$', 'siteapps_v1.bibledb.views.display_chapters', name='browse-kjv-chapters'),
    url(r'^bible/(?P<bookname>[0-9]?(-?[a-zA-Z]+)+)/(?P<chpnum>[0-9]+)/$', 
        'siteapps_v1.bibledb.views.display_verses', name='browse-kjv-verses'),
    url(r'^bible/(?P<bookname>[0-9]?(-?[a-zA-Z]+)+)/(?P<chpnum>[0-9]+)/(?P<startverse>[0-9]+)-?(?P<endverse>[0-9]+)?/$', 
        'siteapps_v1.bibledb.views.display_verses', name='browse-kjv-passage'),
    
    # adding content
    # url(r'^add/entry/$', 'siteapps_v1.bibledb.views.add_content', {'type': 'entry'}, name='add-entry'),
    # url(r'^add/category/$', 'siteapps_v1.bibledb.views.add_content', {'type': 'verse_list'}, name='add-list'),
    
    # feeds
    url(r'^rss/entries/$', RecentEntriesFeed(), name='rss-entries'),
    url(r'^atom/entries/$', RecentEntriesAtomFeed(), name='atom-entries'),
    url(r'^rss/comments/$', RecentCommentsFeed(), name='rss-comments'),
    url(r'^atom/comments/$', RecentCommentsAtomFeed(), name='atom-comments'),

    # ajax urls
    url(r'^ajax/passage/(?P<bookname>[0-9]?( ?[a-zA-Z]+)+)/(?P<chpnum>[0-9]+)/(?P<startverse>[0-9]+)-?(?P<endverse>[0-9]+)?/$', 
        'siteapps_v1.bibledb.views.ajax_passage', name='ajax-passage'),
)