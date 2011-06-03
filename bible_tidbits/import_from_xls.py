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
   
filename = "data/bible_tidbits.txt"
# tidbit_col = 0
# reflection_col = 1
# question_col = 2

f = open(filename,'r')
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
    tidbit.created_by = User.objects.get(username__iexact="leehsueh")
    
    cfs = []
    for cf_str in cfs_list:
        sv = Verse.objects.get(book__iexact=book, chapter_ref__exact=startchp, verse_ref__exact=startverse)
        if not endverse:
            ev = sv
        else:
            ev = Verse.objects.get(book__iexact=book, chapter_ref__exact=endchp, verse_ref__exact=sendverse)
        
        try:
            cross_ref = CrossRef.objects.get(startverse=sv, endverse=ev)
        except CrossRef.DoesNotExist:
            cross_ref = CrossRef(startverse=sv, endverse=ev)
            cross_ref.save()
        cfs.append(cross_ref)
    
f.close()