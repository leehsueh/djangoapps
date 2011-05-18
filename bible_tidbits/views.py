from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from siteapps_v1.bible_tidbits.models import *
import re
from django.utils import simplejson

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

@login_required
def my_tidbits(request):
    c = {
        'tidbits': Tidbit.objects.filter(created_by=request.user),
    }
    return render_to_response("tidbits_home.html", c,
                            context_instance=RequestContext(request))
    
@login_required
def process_tidbit_form(request, tidbit_id=None):
    """
    params are the request parameters; mode is either "edit" or "add"
    """
    params = dict(request.POST) # values are lists
    keys = params.keys()
    if 'tidbit' not in keys or 'cf' not in keys:
        return HttpResponse("Missing parameters.")

    # get form values
    tidbit = params['tidbit'][0]
    is_question = 'is_question' in keys
    if 'more' in keys:
        reflection = params['more'][0]
    else:
        reflection = None

    # filter out blank cf's
    crossrefs = [cf.strip() for cf in params['cf'] if cf != u'']
    if tidbit == u'' or crossrefs == []:
        return HttpResponse("Tidbit and at least one cf is required.")

    # extract tags
    if 'tags' in keys:
        tags = [t.strip() for t in params['tags'][0].split(',') if t.strip() != u'']
    else:
        tags = []

    # create new Tidbit if id not supplied
    if tidbit_id == None:
        tidbit_obj = Tidbit()
    else:
        try:
            tidbit_obj = Tidbit.objects.get(id=tidbit_id)
        except Tidbit.DoesNotExist:
            return HttpResponse("Tidbit not found!")

    tidbit_obj.tidbit = tidbit
    if reflection:
        tidbit_obj.reflection = reflection
    tidbit_obj.is_question = is_question

    tidbit_obj.created_by = request.user

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

    # create tag objects
    tags_to_add = []
    for tag in tags:
        try:
            t = Tag.objects.get(tag=tag)
        except Tag.DoesNotExist:
            t = Tag()
            t.tag = tag
            t.save()
        tags_to_add.append(t)

    # save tidbit to generate a PK before adding cfs via m2m relation
    tidbit_obj.save()

    # clear tags and crossrefs if updating
    if tidbit_id:
        tidbit_obj.cross_refs.clear()
        tidbit_obj.tags.clear()
        
    for cf in cfs_to_add:
        tidbit_obj.cross_refs.add(cf)
    for tag in tags_to_add:
        tidbit_obj.tags.add(tag)
    tidbit_obj.save()

    if not tidbit_id:
        # redirect to home
        return HttpResponseRedirect(reverse("tidbits:home"))
    else:
        c = {
            'tidbit': tidbit_obj,
            'action_url': reverse("tidbits:edit", kwargs={'tidbit_id': tidbit_obj.id})
        }
        return render_to_response("tidbits_edittidbit.html", c, context_instance=RequestContext(request))

@login_required
def add(request):
    """Render form for adding a tidbit"""
    if request.method == 'POST':
        return process_tidbit_form(request)

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
            return process_tidbit_form(request, tidbit_id)
        else:
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

def ajax_tags(request):
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'term'):
            term = request.GET[u'term']
            # Ignore queries shorter than length 3
            if len(term) >= 2:
                model_results = Tag.objects.filter(tag__icontains=term)
                results = [ x.tag for x in model_results ]
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')