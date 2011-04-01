from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from siteapps_v1.bible_tidbits.models import *
import re

def test_form(request):
    import pdb; pdb.set_trace()
    return render_to_response("testform.html", 
                            context_instance=RequestContext(request))

def home(request):
    """The home view"""
    c = {
        'tidbits': Tidbit.objects.all(),
    }
    return render_to_response("home.html", c,
                            context_instance=RequestContext(request))

@login_required
def add(request):
    """Render form for adding a tidbit"""
    if request.method == 'POST':
        params = dict(request.POST)
        import pdb; pdb.set_trace()
        tidbit = params['tidbit']
        crossrefs = params['cf']    # a list if more than one sent
        if isinstance(crossrefs, str):
            crossrefs = list(crossrefs)

        newtidbit = Tidbit()
        newtidbit.tidbit = tidbit
        newtidbit.created_by = request.user
        newtidbit.save()    # need to save before adding cross refs
        
        # create cross reference passage
        regex = re.compile("(?P<book>([12]?[A-Za-z ]+[A-Za-z]))( ?(?P<start_chapter>[0-9]+)((:(?P<start_verse>[0-9]+))? ?(- ?(?P<end_chp_or_verse>[0-9]+)(:(?P<end_verse>[0-9]+))?)?)?)?")
        for cf in crossrefs:
            matches = regex.search(crossref)
            if matches == None:
                continue
            groups = matches.groupdict()
            book = groups['book']
            startchp = groups['start_chapter']
            startvs = groups['start_verse']
            endchporvs = groups['end_chp_or_verse']
            endvs = groups['end_verse']
    
            if not endchporvs:
                endchp = startchp
                endvs = startvs
            if not endvs:
                endvs = endchporvs
                endchp = startchp
            else:
                endchp = endchporvs
    
            startverse = Verse.objects.get(book__iexact=book,
                                            chapter_ref=int(startchp),
                                            verse_ref=int(startvs))
            endverse = Verse.objects.get(book__iexact=book,
                                            chapter_ref=int(endchp),
                                            verse_ref=int(endvs))
            # check for existing cf
            try:
                cf = CrossRef.objects.get(startverse=startverse, endverse=endverse)
                newtidbit.cross_refs.add(cf)
            except CrossRef.DoesNotExist:
                newcf = CrossRef()
                newcf.startverse = startverse
                newcf.endverse = endverse
                newcf.save()
                newtidbit.cross_refs.add(newcf)
        
        newtidbit.save()
        
        # redirect to home
        return HttpResponseRedirect(reverse("tidbits:home"))

    else:
        return render_to_response("addtidbit.html", context_instance=RequestContext(request))

@login_required
def edit(request, tidbit_id):
    """Edit a tidbit."""
    try:
        tidbit = Tidbit.objects.get(id=tidbit_id)
        return HttpResponse(tidbit.tidbit)
    except Tidbit.DoesNotExist:
        return HttpResponse("Tidbit not found!")