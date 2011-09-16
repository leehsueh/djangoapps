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

class CrossRefManager(models.Manager):
    def parse_reference(self, passage_ref):
        regex = re.compile("(?P<book>([12]?[A-Za-z ]+[A-Za-z]))( ?(?P<start_chapter>[0-9]+)((:(?P<start_verse>[0-9]+))? ?(- ?(?P<end_chp_or_verse>[0-9]+)(:(?P<end_verse>[0-9]+))?)?)?)?$")
        matches = regex.search(passage_ref)
        if matches == None:
            # TODO: make this neater
            raise Exception("Regex failed")
        groups = matches.groupdict()
        book = groups['book']
        startchp = groups['start_chapter']
        startvs = groups['start_verse']
        endchporvs = groups['end_chp_or_verse']
        endvs = groups['end_verse']
        
        # validate book
        if Verse.objects.filter(book__istartswith=book).count() == 0:
            raise Exception("Book " + book + " is invalid")
        else:
            book = Verse.objects.filter(book__istartswith=book)[0].book

        if not startchp:
            startchp = 1
            startvs = 1
            lastverse = Verse.objects.filter(
                            book__iexact=book,
                        ).order_by('-id')[:1]
            endchp = lastverse[0].chapter_ref
            endvs = lastverse[0].verse_ref
        elif not startvs:
            startvs = 1
            lastverse = Verse.objects.filter(
                            book__iexact=book,
                            chapter_ref=int(startchp)
                        ).order_by('-id')[:1]
            if lastverse.count() == 0:
                raise Exception(book + " " + startchp + " is invalid")
            endchp = lastverse[0].chapter_ref
            endvs = lastverse[0].verse_ref
        elif not endchporvs:
            endchp = startchp
            endvs = startvs
        elif not endvs:
            endvs = endchporvs
            endchp = startchp
        else:
            endchp = endchporvs
        
        try:
            startverse = Verse.objects.get(book__istartswith=book,
                                                chapter_ref=int(startchp),
                                                verse_ref=int(startvs))
            endverse = Verse.objects.get(book__istartswith=book,
                                                chapter_ref=int(endchp),
                                                verse_ref=int(endvs))
            if startverse.id > endverse.id:
                # TODO: handle this
                raise Exception("Start verse must be before end verse.")
        except Verse.DoesNotExist as e:
            raise Exception(passage_ref + " is invalid.")
        return (startverse, endverse)

class CrossRef(models.Model):
    """Encapsulates a "passage" or "cross reference."
    startverse should be before endverse. If there is only one verse,
    then startverse = endverse (neither should be null). In addition,
    should restrict that both verses be contained in the same book.
    """

    startverse = models.ForeignKey(Verse, related_name="startverse")
    endverse = models.ForeignKey(Verse, related_name="endverse")

    # custom manager
    objects = CrossRefManager()

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