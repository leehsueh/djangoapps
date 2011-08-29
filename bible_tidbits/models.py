from django.db import models
from django.contrib.auth.models import User
import re

class Verse(models.Model):
    book = models.CharField(max_length=64, editable=False)
    chapter_ref = models.IntegerField(editable=False)
    verse_ref = models.IntegerField(editable=False)

    def __unicode__(self):
        return u'%s %s:%s' % (self.book, self.chapter_ref, self.verse_ref)

    class Meta:
        ordering = ['id']

class CrossRef(models.Model):
    """Encapsulates a "passage" or "cross reference."
    startverse should be before endverse. If there is only one verse,
    then startverse = endverse (neither should be null). In addition,
    should restrict that both verses be contained in the same book.
    """

    startverse = models.ForeignKey(Verse, related_name="startverse")
    endverse = models.ForeignKey(Verse, related_name="endverse")

    def __unicode__(self):
        if self.startverse.id == self.endverse.id:
            return u'%s %s:%s' % (self.startverse.book, self.startverse.chapter_ref,
                                  self.startverse.verse_ref)
        elif self.startverse.chapter_ref == self.endverse.chapter_ref:
            return u'%s %s:%s-%s' % (self.startverse.book, self.startverse.chapter_ref,
                                     self.startverse.verse_ref, self.endverse.verse_ref)
        else:
            return u'%s %s:%s-%s:%s' % (self.startverse.book,
                                self.startverse.chapter_ref, self.startverse.verse_ref,
                                self.endverse.chapter_ref, self.endverse.verse_ref)
    class Meta:
        ordering = ['startverse', 'endverse']
        unique_together = ('startverse', 'endverse')
        verbose_name = "Cross Reference"

class Tag(models.Model):
    tag = models.CharField(max_length=128)
    slug = models.SlugField(max_length=50, unique=True)
    category = models.CharField(max_length=128, blank=True, null=True)

    regex = re.compile(r'[^a-zA-Z0-9-]')

    def __unicode__(self):
        if self.category != None and self.category != u'':
            return self.category + u': ' + self.tag
        else:
            return self.tag
    
    def save(self, *args, **kwargs):
        if (self.tag and self.category):
            s = (self.category + ' ' + self.tag).strip().lower().replace(' ','-')
        else:
            s = self.tag.strip().lower().replace(' ','-')
        self.slug = re.sub(self.regex, '', s)
        super(Tag, self).save(*args, **kwargs)
    
    class Meta:
        unique_together = ('tag', 'category')

class Tidbit(models.Model):
    tidbit = models.TextField()
    cross_refs = models.ManyToManyField(CrossRef)
    reflection = models.TextField(blank=True, null=True)
    is_question = models.BooleanField()
    tags = models.ManyToManyField(Tag)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return u'%s, by %s' % (self.tidbit[:50], self.created_by.username)
        
    class Meta:
        ordering = ['-updated_on', '-created_on', '-id']