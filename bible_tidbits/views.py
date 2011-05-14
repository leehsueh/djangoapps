from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from siteapps_v1.bible_tidbits.models import *
import re

def test_form(request):
    return render_to_response("testform.html", 
                            context_instance=RequestContext(request))

def home(request):
    """The home view"""
    c = {
        'tidbits': Tidbit.objects.all(),
    }
    return render_to_response("tidbits_home.html", c,
                            context_instance=RequestContext(request))

def add(request):
    """Render form for adding a tidbit"""
    if request.method == 'POST':
        params = dict(request.POST) # values are lists
        #import pdb; pdb.set_trace()
        # check for required parameters
        keys = params.keys()
        if 'tidbit' not in keys or 'cf' not in keys:
            return HttpResponse("Missing parameters.")
        
        tidbit = params['tidbit'][0]
        is_question = 'is_question' in keys
        if 'more' in keys:
            reflection = params['more'][0]
        
        # filter out blank cf's
        crossrefs = [cf for cf in params['cf'] if cf != u'']
        if tidbit == u'' or crossrefs == []:
            return HttpResponse("Tidbit and at least one cf is required.")

        # required values populated; create new Tidbit
        newtidbit = Tidbit()
        newtidbit.tidbit = tidbit
        if reflection:
            newtidbit.reflection = reflection
        newtidbit.is_question = is_question
        
        newtidbit.created_by = request.user
        
        # add and/or create cross references
        cfs_to_add = []
        regex = re.compile("(?P<book>([12]?[A-Za-z ]+[A-Za-z]))( ?(?P<start_chapter>[0-9]+)((:(?P<start_verse>[0-9]+))? ?(- ?(?P<end_chp_or_verse>[0-9]+)(:(?P<end_verse>[0-9]+))?)?)?)?$")
        for cf in crossrefs:
            matches = regex.search(cf)
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
                return HttpResponse("A cf is invalid: " + cf)
            
            # check for existing cf
            try:
                cf = CrossRef.objects.get(startverse=startverse, endverse=endverse)
                cfs_to_add.append(cf)
            except CrossRef.DoesNotExist:
                newcf = CrossRef()
                newcf.startverse = startverse
                newcf.endverse = endverse
                newcf.save()
                cfs_to_add.append(newcf)

        # save tidbit to generate a PK before adding cfs via m2m relation
        newtidbit.save()
        for cf in cfs_to_add:
            newtidbit.cross_refs.add(cf)
        newtidbit.save()
        
        # redirect to home
        return HttpResponseRedirect(reverse("tidbits:home"))

    else:
        c = {
            'action_url': reverse("tidbits:add"),
        }
        return render_to_response("tidbits_edittidbit.html", c, context_instance=RequestContext(request))

@login_required
def edit(request, tidbit_id):
    """Edit a tidbit."""
    # TODO: refactor this logic (same as add logic)
    try:
        tidbit = Tidbit.objects.get(id=tidbit_id)
        if not tidbit.created_by == request.user:
            return HttpResponse("You are not authorized to edit this Tidbit.")
        
        if request.method == 'POST':
            params = dict(request.POST) # values are lists
            
            # check for required parameters
            keys = params.keys()
            if 'tidbit' not in keys or 'cf' not in keys:
                return HttpResponse("Missing parameters.")

            updated_tidbit = params['tidbit'][0]
            updated_is_question = 'is_question' in keys
            if 'more' in keys:
                updated_reflection = params['more'][0]

            # filter out blank cf's
            updated_crossrefs = [cf for cf in params['cf'] if cf != u'']
            if updated_tidbit == u'' or updated_crossrefs == []:
                return HttpResponse("Tidbit and at least one cf is required.")

            # required values populated; update Tidbit
            tidbit.tidbit = updated_tidbit
            if updated_reflection:
                tidbit.reflection = updated_reflection
            tidbit.is_question = updated_is_question


            # add and/or create cross references
            cfs_to_add = []
            regex = re.compile("(?P<book>([12]?[A-Za-z ]+[A-Za-z]))( ?(?P<start_chapter>[0-9]+)((:(?P<start_verse>[0-9]+))? ?(- ?(?P<end_chp_or_verse>[0-9]+)(:(?P<end_verse>[0-9]+))?)?)?)?$")
            for cf in updated_crossrefs:
                matches = regex.search(cf)
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
                    return HttpResponse("A cf is invalid: " + cf)

                # check for existing cf
                try:
                    cf = CrossRef.objects.get(startverse=startverse, endverse=endverse)
                    cfs_to_add.append(cf)
                except CrossRef.DoesNotExist:
                    newcf = CrossRef()
                    newcf.startverse = startverse
                    newcf.endverse = endverse
                    newcf.save()
                    cfs_to_add.append(newcf)

            # clear cfs
            tidbit.cross_refs.clear()

            # add updated cfs
            for cf in cfs_to_add:
                tidbit.cross_refs.add(cf)
            tidbit.save()

        c = {
            'tidbit': tidbit,
            'action_url': reverse("tidbits:edit", kwargs={'tidbit_id': tidbit.id})
        }
        return render_to_response("tidbits_edittidbit.html", c, context_instance=RequestContext(request))
    
    except Tidbit.DoesNotExist:
        return HttpResponse("Tidbit not found!")

@login_required
def delete(request, tidbit_id):
    """Delete a tidbit."""
    try:
        tidbit = Tidbit.objects.get(id=tidbit_id)
        tidbit.delete()
        return HttpResponseRedirect(reverse("tidbits:home"))
    except Tidbit.DoesNotExist:
        return HttpResponse("Tidbit not found!")

def tidbits_by_book(request, book):
    book = book.replace('-',' ')
    firstverse = Verse.objects.filter(book__iexact=book).order_by('id')[:1]
    if firstverse.count() == 0:
        return HttpResponse(book + " is not valid!")
    lastverse = Verse.objects.filter(book__iexact=book).order_by('-id')[:1]
    cfs = CrossRef.objects.filter(startverse__gte=firstverse, endverse__lte=lastverse)

    from django.db.models.query import EmptyQuerySet
    tidbits = EmptyQuerySet()
    for cf in cfs:
        tidbits |= cf.tidbit_set.all()

    c = {
        'filter_criteria': book,
        'tidbits': tidbits,
    }
    return render_to_response("tidbits_home.html", c, context_instance=RequestContext(request))