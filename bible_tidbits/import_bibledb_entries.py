# importing bibledb entries into bible tidbits
from siteapps_v1.bibledb.models import *
from siteapps_v1.bible_tidbits.models import *

entries = Entry.objects.all()
for entry in entries:
    if entry.title == '' or entry.title == None:
        continue
    tidbit = entry.title
    reflection = entry.context_notes + entry.notes
    print reflection
    sv_id = entry.startverse.id + 1 # bible_tidbits_verse table id starts at 2...
    if entry.endverse:
        ev_id = entry.endverse.id + 1
    else:
        ev_id = sv_id
    sv = Verse.objects.get(id=sv_id)
    ev = Verse.objects.get(id=ev_id)
    
    try:
        cross_ref = CrossRef.objects.get(startverse=sv, endverse=ev)
    except CrossRef.DoesNotExist:
        cross_ref = CrossRef(startverse=sv, endverse=ev)
        cross_ref.save()
        
    tags = []
    for cat in entry.categories.all():
        if cat != 'Uncategorized':
            tags.append(cat.category)
    for t in entry.tags.all():
        tags.append(t.name)
        
    new_tidbit = Tidbit()
    new_tidbit.tidbit = tidbit
    new_tidbit.reflection = reflection
    new_tidbit.created_by = entry.created_by    
    new_tidbit.save()

    new_tidbit.created_on = entry.pub_date
    new_tidbit.updated_on = entry.created_by
    
    new_tidbit.cross_refs.add(cross_ref)
    for tag in tags:
        try:
            t = Tag.objects.get(tag__exact=tag)
        except Tag.DoesNotExist:
            t = Tag(tag=tag)
            t.save()
        new_tidbit.tags.add(t)