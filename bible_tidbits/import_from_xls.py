from siteapps_v1.bible_tidbits.models import *
from django.contrib.auth.models import User
import re

def filter_quotes(s):
    s = s.strip()
    if len(s) < 2:
        return s
    if s[0] == '"' and s[-1] == '"':
        return s[1:-1].replace('""','"')
    else:
        return s
   
filename = "bible_tidbits/data/bible_tidbits.tsv"
# tidbit_col = 0
# reflection_col = 1
# question_col = 2

f = open(filename,'r')
f.readline()
for line in f:
    if line.strip() == '':
        continue
    parts = line.split("\t")
    tidbit_str = filter_quotes(parts[0])
    reflection_str = filter_quotes(parts[1])
    question = parts[2].strip() != ''
    cfs_list = [ cf for cf in parts[3:] if cf.strip() != ''] 
    
    tidbit = Tidbit()
    tidbit.tidbit = tidbit_str
    tidbit.reflection = reflection_str
    tidbit.is_question = question
    tidbit.created_by = User.objects.get(username__iexact="leehsueh")

    # print tidbit.tidbit, tidbit.reflection, tidbit.is_question
    
    cfs = []
    regex = re.compile("(?P<book>([12]?[A-Za-z ]+[A-Za-z]))( ?(?P<start_chapter>[0-9]+)((:(?P<start_verse>[0-9]+))? ?(- ?(?P<end_chp_or_verse>[0-9]+)(:(?P<end_verse>[0-9]+))?)?)?)?$")
    for cf_str in cfs_list:
        # print cf_str
        matches = regex.search(cf_str)
        if matches == None:
            continue
        groups = matches.groupdict()
        book = groups['book']
        startchp = groups['start_chapter']
        startvs = groups['start_verse']
        endchporvs = groups['end_chp_or_verse']
        endvs = groups['end_verse']

        if not startvs:
            # only book and chapter specified
            startvs = 1
            endchp = startchp
            endvs = Verse.objects.filter(book__istartswith=book, chapter_ref=int(startchp)).order_by('-verse_ref')[0].verse_ref
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
        except Verse.DoesNotExist:
            print "Error: " + cf_str + " is invalid"

        # check for existing cf
        try:
            cf = CrossRef.objects.get(startverse=startverse, endverse=endverse)
            cfs.append(cf)
        except CrossRef.DoesNotExist:
            newcf = CrossRef()
            newcf.startverse = startverse
            newcf.endverse = endverse
            newcf.save()
            cfs.append(newcf)
    
    tidbit.save()
    for cf in cfs:
        tidbit.cross_refs.add(cf)
    tidbit.save()
    
f.close()