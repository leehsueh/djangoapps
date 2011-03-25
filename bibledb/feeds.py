from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from siteapps_v1.bibledb.models import Entry
from django.contrib.comments import Comment
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

class RecentEntries(Feed):
    title = "BibleDB Recent Entries Feed"
    link = "/feeds/latest/"
    description = "Latest entries posted on BibleDB"

    def items(self):
        return Entry.objects.filter(removed=False).order_by('-pub_date')[:5]
        
    def item_link(self, item):
        return reverse('bibledb:entry-view',kwargs={'entry_id': item.id})
        
class RecentEntriesAtom(RecentEntries):
    feed_type = Atom1Feed
    subtitle = RecentEntries.description
    
class RecentComments(Feed):
    title = "BibleDB Recent Comments Feed"
    link = "/feeds/comments/"
    description = "Latest comments posted on BibleDB"

    def items(self):
        return Comment.objects.filter(content_type=ContentType.objects.get(model__iexact='Entry')).exclude(is_removed=True).order_by('-submit_date')[:5]
        
    def item_link(self, item):
        return reverse('bibledb:entry-view',kwargs={'entry_id': item.content_object.id})
        
class RecentCommentsAtom(RecentComments):
    feed_type = Atom1Feed
    subtitle = RecentEntries.description