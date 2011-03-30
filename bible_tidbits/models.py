from django.db import models

class Verse(models.Model):
    book = models.CharField(max_length=64, editable=False)
    chapter_ref = models.IntegerField(editable=False)
    verse_ref = models.IntegerField(editable=False)

    def __unicode__(self):
        return u'%s %s:%s' % (self.book, self.chapter_ref, self.verse_ref)

    class Meta:
        ordering = ['id']

class CrossRef(models.Model):
    """Encapsulates a "passage" or "cross reference.
    startverse should be before endverse. If there is only one verse,
    then startverse = endverse (neither should be null). In addition,
    should restrict that both verses be contained in the same book.
    """

    startverse = models.ForeignKey(Verse, related_name="startverse")
    endverse = models.ForeignKey(Verse, related_name="endverse")

    def __unicode__(self):
        if startverse.id == endverse.id:
            return u'%s %s:%s' % (startverse.book, startverse.chapter_ref,
                                  startverse.verse_ref)
        elif startverse.chapter_ref == endverse.chapter_ref:
            return u'%s %s:%s-%s' % (startverse.book, startverse.chapter_ref,
                                     startverse.verse_ref, endverse.verse_ref)
        else:
            return u'%s %s:%s-%s:%s' % (startverse.book,
                                startverse.chapter_ref, startverse.verse_ref,
                                endverse.chapter_ref, endverse.verse_ref)