from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from siteapps_v1.bible_tidbits.models import *
import re
from django.utils import simplejson

# TODO: refactor total_count into common context processor

def paginate_tidbits(request, tidbit_qs):
    """ returns the paginator for the given query set"""
    paginator = Paginator(tidbit_qs, 10)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        tidbits = paginator.page(page)
    except (EmptyPage, InvalidPage):
        tidbits = paginator.page(paginator.num_pages)

    return tidbits

def home(request):
    """The home view"""
    tidbits_qs = Tidbit.objects.all()
    tidbits = paginate_tidbits(request, tidbits_qs)
    c = {
        'tidbits': tidbits,
        'total_count': tidbits_qs.count()
    }
    return render_to_response("tidbits_home.html", c,
                            context_instance=RequestContext(request))

def tidbit_detail(request, tidbit_id):
    try:
        tidbit = Tidbit.objects.get(pk=tidbit_id)
    except Tidbit.DoesNotExist:
        raise Http404("Oops! This tidbit does not exist!")
    c = {
        'tidbit': tidbit,
    }
    return render_to_response("tidbits_detail.html", c,
                            context_instance=RequestContext(request))

def tidbits_by_user(request, username):
    try:
        user = User.objects.get(username__iexact=username)
        tidbit_qs = Tidbit.objects.filter(created_by=user)
        c = {
            'tidbits': paginate_tidbits(request, tidbit_qs),
            'filter_criteria': username,
            'filter_count': tidbit_qs.count(),
            'total_count': Tidbit.objects.all().count()
        }
        return render_to_response("tidbits_home.html", c,
                            context_instance=RequestContext(request))
    except User.DoesNotExist:
        return HttpResponse("User " + username + " is not valid.")

@login_required
def my_tidbits(request):
    tidbits_qs = Tidbit.objects.filter(created_by=request.user)
    c = {
        'tidbits': paginate_tidbits(request, tidbits_qs),
        'filter_count': tidbits_qs.count(),
        'filter_criteria': request.user.username,
        'total_count': Tidbit.objects.all().count()
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

    # extract bible study tags
    if 'bible_study_tags' in keys:
        bible_study_tag_ids = [int(tid) for tid in params['bible_study_tags']]
    else:
        bible_study_tag_ids = []

    # create new Tidbit if id not supplied
    if tidbit_id == None:
        tidbit_obj = Tidbit()
    else:
        try:
            tidbit_obj = Tidbit.objects.get(id=tidbit_id)
        except Tidbit.DoesNotExist:
            return HttpResponse("Tidbit not found!")

    tidbit_obj.tidbit = tidbit
    if reflection != None and reflection != u'':
        tidbit_obj.reflection = reflection
    else:
        tidbit_obj.reflection = None
    tidbit_obj.is_question = is_question

    tidbit_obj.created_by = request.user

    # add and/or create cross references
    cfs_to_add = []
    for cf in crossrefs:
        try:
            startverse, endverse = CrossRef.objects.parse_reference(cf)
        except Exception as e:
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
            t = Tag.objects.get(tag__iexact=tag, category=None)
        except Tag.DoesNotExist:
            t = Tag()
            t.tag = tag
            t.save()
        tags_to_add.append(t)
    
    # TODO: handle bible study tags; append to tags_to_add
    for tag_id in bible_study_tag_ids:
        try:
            t = Tag.objects.get(pk=tag_id)
            tags_to_add.append(t)
        except Tag.DoesNotExist:
            pass


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
            'bible_study_tags': Tag.objects.filter(category__iexact=u'bible study'),
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
            'bible_study_tags': Tag.objects.filter(category__iexact=u'bible study'),
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
                'bible_study_tags': Tag.objects.filter(category__iexact=u'bible study'),
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
    startverse = Verse.objects.filter(book__iexact=book).order_by('id')[:1]
    if startverse.count() == 0:
        return HttpResponse(book + " is not valid!")
    endverse = Verse.objects.filter(book__iexact=book).order_by('-id')[:1]
    cfs = CrossRef.objects.filter(startverse__gte=startverse, endverse__lte=endverse)

    from django.db.models.query import EmptyQuerySet
    tidbits = EmptyQuerySet()
    for cf in cfs:
        tidbits |= cf.tidbit_set.all()
    tidbits = tidbits.distinct()
    c = {
        'filter_criteria': book,
        'filter_count': tidbits.count(),
        'tidbits': paginate_tidbits(request, tidbits),
        'total_count': Tidbit.objects.all().count()
    }
    return render_to_response("tidbits_home.html", c, context_instance=RequestContext(request))

def tidbits_by_tag(request, tag_slug):
    try:
        tag = Tag.objects.get(slug__exact=tag_slug)
    except:
        return HttpResponse("Does not exist!")

    from django.db.models.query import EmptyQuerySet
    tidbits = tag.tidbit_set.all()

    c = {
        'filter_criteria': tag.tag,
        'tidbits': paginate_tidbits(request, tidbits),
        'filter_count': tidbits.count(),
        'total_count': Tidbit.objects.all().count()
    }
    return render_to_response("tidbits_home.html", c, context_instance=RequestContext(request))

def question_tidbits(request):
    tidbits_qs = Tidbit.objects.filter(is_question=True)
    c = {
        'filter_criteria': 'marked as question',
        'tidbits': paginate_tidbits(request, tidbits_qs),
        'filter_count': tidbits_qs.count(),
        'total_count': Tidbit.objects.all().count()
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
    
def ajax_bible_text(request):
    if request.method == 'GET':
        if request.GET.has_key(u'passage'):
            req_params = dict()
            req_params['passage'] = request.GET[u'passage']
            import siteapps_v1.biblia as Biblia
            result_tuple = Biblia.content('KJV', ext='txt', request_params=req_params)
            if result_tuple['success']:
                return HttpResponse(result_tuple['response'])
            else:
                return HttpResponse('Could not get passage ' + req_params['passage'] + ': ' + result_tuple['response'])
        else:
            return HttpResponse('passage parameter missing')
    else:
        return HttpResponse('Request method should be GET')

def tidbits_by_passage(request, user=None):
    if request.method == 'GET':
        passage_ref = request.GET['passage_ref']
        try:
            startverse, endverse = CrossRef.objects.parse_reference(passage_ref)
        except Exception as e:
            # TODO: make this neater
            return HttpResponse(str(e.args[0]))

        # regex = re.compile("(?P<book>([12]?[A-Za-z ]+[A-Za-z]))( ?(?P<start_chapter>[0-9]+)((:(?P<start_verse>[0-9]+))? ?(- ?(?P<end_chp_or_verse>[0-9]+)(:(?P<end_verse>[0-9]+))?)?)?)?$")
        # matches = regex.search(passage_ref)
        # if matches == None:
        #     # TODO: make this neater
        #     return HttpResponse("Invalid passage reference: " + passage_ref)
        # groups = matches.groupdict()
        # book = groups['book']
        # startchp = groups['start_chapter']
        # startvs = groups['start_verse']
        # endchporvs = groups['end_chp_or_verse']
        # endvs = groups['end_verse']
        # cfs = None
        
        # if not startchp:
        #     startverse = Verse.objects.filter(book__iexact=book).order_by('id')[:1]
        #     if startverse.count() == 0:
        #         return HttpResponse(book + " is not valid!")
        #     endverse = Verse.objects.filter(book__iexact=book).order_by('-id')[:1]
        #     cfs = CrossRef.objects.filter(startverse__gte=startverse, endverse__lte=endverse)
        # elif not startvs:
        #     startverse = Verse.objects.filter(
        #                     book__iexact=book, 
        #                     chapter_ref=int(startchp), 
        #                     verse_ref=1
        #                 ).order_by('id')[:1]
        #     if startverse.count() == 0:
        #         return HttpResponse(book + " " + int(startchp) + " is not valid!")
        #     endverse = Verse.objects.filter(
        #                     book__iexact=book,
        #                     chapter_ref=int(startchp)
        #                 ).order_by('-id')[:1]
        #     cfs = CrossRef.objects.filter(startverse__gte=startverse, endverse__lte=endverse)
        # elif not endchporvs:
        #     endchp = startchp
        #     endvs = startvs
        # elif not endvs:
        #     endvs = endchporvs
        #     endchp = startchp
        # else:
        #     endchp = endchporvs

        # startverse = Verse.objects.get(book__istartswith=book,
        #                                 chapter_ref=int(startchp),
        #                                 verse_ref=int(startvs))
        # endverse = Verse.objects.get(book__istartswith=book,
        #                                 chapter_ref=int(endchp),
        #                                 verse_ref=int(endvs))
        # if startverse.id > endverse.id:
        #     # TODO: handle this
        #     return HttpResponse("Start verse " + startverse + " must come before end verse " + endverse)

        # get tidbits where a cross ref intersects with a given range (more general)
        cfs = CrossRef.objects.filter(
                                startverse__gte=startverse, 
                                endverse__lte=endverse
                            )
        cfs |= CrossRef.objects.filter(
                                startverse__gte=startverse, 
                                endverse__gte=endverse, 
                                startverse__lte=endverse
                            )
        cfs |= CrossRef.objects.filter(
                                startverse__lte=startverse, 
                                endverse__lte=endverse, 
                                endverse__gte=startverse
                            )

        # get tidbits where a cross ref is completely contained in the given range (more precise)
        cfs = CrossRef.objects.filter(
                                startverse__gte=startverse, 
                                endverse__lte=endverse
                            )

        # get tidbit entries for each cf

        from django.db.models.query import EmptyQuerySet
        tidbits = EmptyQuerySet()
        for cf in cfs:
            tidbits |= cf.tidbit_set.all()
        tidbits = tidbits.distinct()
    else:
        return HttpResponseRedirect(reverse('tidbits:home'))
    c = {
        'filter_criteria': passage_ref,
        'filter_count': tidbits.count(),
        'tidbits': paginate_tidbits(request, tidbits),
        'total_count': Tidbit.objects.all().count()
    }
    return render_to_response("tidbits_home.html", c, context_instance=RequestContext(request))
