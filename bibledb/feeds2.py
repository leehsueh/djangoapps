# feeds2.py: updated Feed classes for Django 1.2+

__author__="leehsueh"
__date__ ="$Feb 1, 2011 8:24:22 PM$"

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from siteapps_v1.bibledb.models import Entry
from django.contrib.comments import Comment
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

class RecentEntriesFeed(Feed):
    title = "BibleDB Recent Entries Feed"
    link = ""
    description = "Latest entries posted on BibleDB"

    def items(self):
        return Entry.objects.filter(removed=False).order_by('-pub_date')[:5]

    def item_link(self, item):
        return reverse('bibledb:entry-view',kwargs={'entry_id': item.id})

    def item_title(self, item):
        if item.title:
            return item.title + u', ' + item.get_book() + u' ' + item.get_passage_ref()
        else:
            return u'(Untitled...)'

    def item_description(self, item):
        html = u''
        if item.context_notes:
            html += u'<b>Context notes:</b><p>' + item.context_notes + u'</p>'
        if item.notes:
            html += u'<b>Reflections:</b><p>' + item.notes + u'</p>'
        html += u'<p><em>Posted by ' + item.created_by.username + u' on ' + item.pub_date.strftime("%m/%d/%Y") + u'.</em></p>'
        return html

class RecentEntriesAtomFeed(RecentEntriesFeed):
    feed_type = Atom1Feed
    subtitle = RecentEntriesFeed.description

class RecentCommentsFeed(Feed):
    title = "BibleDB Recent Comments Feed"
    link = ""
    description = "Latest comments posted on BibleDB"

    def items(self):
        return Comment.objects.filter(content_type=ContentType.objects.get(model__iexact='Entry')).exclude(is_removed=True).order_by('-submit_date')[:5]

    def item_link(self, item):
        return reverse('bibledb:entry-view',kwargs={'entry_id': item.content_object.id})

    def item_title(self, item):
        return item.user.username + u' commented on ' + item.content_object.title

    def item_description(self, item):
        html = u'<p><strong>Related Passage:</strong> '
        html += item.content_object.get_book() + ' ' + item.content_object.get_passage_ref() + u'</p>'
        html += u'<blockquote>' + item.comment + u'</blockquote>'
        return html

class RecentCommentsAtomFeed(RecentCommentsFeed):
    feed_type = Atom1Feed
    subtitle = RecentCommentsFeed.description
