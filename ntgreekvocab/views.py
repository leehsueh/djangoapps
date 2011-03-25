import siteapps_v1.ntgreekvocab.models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from siteapps_v1.ntgreekvocab.models import SimpleCard
from siteapps_v1.ntgreekvocab.forms import SimpleCardAdminForm
from siteapps_v1.ntgreekvocab import greek
from django.contrib.auth.decorators import login_required
import random

# choose list containing num random card id's
# TODO: make cleaner
def get_random_ids(request, num, lesson_number=-1, lesson_numbers=[]):
    """if lesson_number is -1, don't filter. if lesson_number is 0, only include words with no lesson number"""
    if num < 1:
        num = 1
    # import pdb;pdb.set_trace()
    if isinstance(lesson_numbers, list):
        if lesson_numbers == ['0',]:
            cards = SimpleCard.objects.filter(lesson_number='')
        else:
            cards = SimpleCard.objects.filter(lesson_number__in=lesson_numbers)
    elif lesson_number == -1:
        cards = SimpleCard.objects.all()
    elif lesson_number == None:
        cards = SimpleCard.objects.filter(lesson_number='') | SimpleCard.objects.filter(lesson_number__isnull=True)
    elif lesson_number:
        cards = SimpleCard.objects.filter(lesson_number__iexact=lesson_number)

    # if lesson_number is invalid or no results, remove filter altogether
    count = cards.count()
    if count < num:
        cards = SimpleCard.objects.all()
        del request.session['ln']
        
    card_ids = cards.values_list('id', flat=True)
    return random.sample(card_ids, num)

# Create your views here.
def clear_session(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('ntgreekvocab:home'))


def home(request):
    # TODO: make cleaner
    if request.GET.has_key(u'ln'):
        request.session['ln'] = request.GET[u'ln'].upper().split(',')
            
    random_ids = get_random_ids(request, 2, lesson_numbers=request.session.get('ln',-1))
    random_card = SimpleCard.objects.get(pk=random_ids[0])
    c = {
        'card': random_card,
        'random_card_id': random_ids[1],
        'def_article': random_card.get_def_article()
    }
    # add the lesson number to the context if filtering by lesson
    if 'ln' in request.session.keys():
        c['lesson_numbers'] = request.session['ln']
        
    return render_to_response('ntgreekvocab/home.html', c, RequestContext(request))

@login_required
def card_edit(request, card_id):
    try:
        card = SimpleCard.objects.get(id=card_id)
    except SimpleCard.DoesNotExist:
        raise Http404("Sorry, card with id " + str(card_id) + " does not exist!")

    if request.method == 'POST':
        form = SimpleCardAdminForm(request.POST)
        if form.is_valid():
            cleandata = form.cleaned_data
            # @type card SimpleCard
            card.greek_word = cleandata['greek_word']
            card.definition = cleandata['definition']
            card.lesson_number = cleandata['lesson_number']
            card.notes = cleandata['notes']
            card.hints = cleandata['hints']
            card.parsing_info = cleandata['parsing_info']
            card.part_of_speech = cleandata['part_of_speech']
            card.related_cards = cleandata['related_cards']
            card.save(force_update=True)
            return HttpResponseRedirect(reverse('ntgreekvocab:card-view', kwargs={'card_id':card.id}))
    else:
        form = SimpleCardAdminForm(instance=card)

    context = {
        'form': form,
        'card': card,
    }
    return render_to_response('ntgreekvocab/editcard.html', context, RequestContext(request))

def card_view(request, card_id):
    try:
        card = SimpleCard.objects.get(id=card_id)
        ln = request.session.get('ln',-1)
        context = { 
            'card': card,
            'random_card_id': get_random_ids(request, 1,lesson_numbers=ln)[0],
            'def_article': card.get_def_article()
        }
        # TODO: make cleaner
        # add the lesson number to the context if filtering by lesson
        if 'ln' in request.session.keys():
            context['lesson_numbers'] = request.session['ln']

        # parameter for initially showing the word info
        if request.GET.has_key('show'):
            context['show_word_info'] = True
        
        return render_to_response('ntgreekvocab/home.html', context, RequestContext(request))
    
    except SimpleCard.DoesNotExist:
        raise Http404("Sorry, card with id " + str(card_id) + " does not exist!")

def card_list(request):
    words_by_letter = []
    total_fetched = 0
    for letter in greek.alphabet.lc_letters:
        letter_qs = SimpleCard.objects.filter(greek_word__istartswith=letter).order_by('greek_word').values('id','greek_word','definition','lesson_number','part_of_speech')
        total_fetched += letter_qs.count()
        words_by_letter.append((letter, letter_qs))

    # build list of tuples (ln_int, ln_str)
    lessons = SimpleCard.objects.all().values_list('lesson_number', flat=True).order_by('lesson_number').distinct()
    tuples_list = []
    for lesson in lessons:
        try:
            tuples_list.append((int(lesson), lesson))
        except:
            if lesson == '18A':
                tuples_list.append((18.1, lesson))
            elif lesson == '18B':
                tuples_list.append((18.2, lesson))
    tuples_list.sort()
    
    # undecorate list of tuples
    lesson_nums = []
    for ln_int, ln_str in tuples_list:
        lesson_nums.append(ln_str)

    parts_of_speech = [(short,long) for short, long in siteapps_v1.ntgreekvocab.models.PARTS_OF_SPEECH_MAP.items()]
    context = {
        'total_fetched': total_fetched,
        'total_words': SimpleCard.objects.all().count(),
        'letters': greek.alphabet.lc_letters,
        'words_by_letter': words_by_letter,
        'lessons': lesson_nums,
        'parts_of_speech': sorted(parts_of_speech)
    }
    return render_to_response('ntgreekvocab/listcards.html', context, RequestContext(request))

def card_lookup(request):
    context = {}
    return render_to_response('ntgreekvocab/lookupcard.html', context, RequestContext(request))

# ajax views
def ajax_card_autocomplete(request):
    # Default return list Will Larson method
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            # Ignore queries shorter than length 3
            if len(value) > 2:
                model_results = SimpleCard.objects.filter(greek_word__icontains=value) | SimpleCard.objects.filter(definition__icontains=value)
                if request.GET.has_key(u'id'):
                    # exclude current card from list
                    card_id = request.GET[u'id']
                    model_results = model_results.exclude(pk=card_id)
                results = [ {'greek_word':x.greek_word, 'definition':x.definition, 'id':x.id} for x in model_results ]
    json = simplejson.dumps(results)
    return HttpResponse(json, mimetype='application/json')

def ajax_card_fetch(request, card_id):
    try:
        card = SimpleCard.objects.get(id=card_id)
        context = {
            'card': card,
            'def_article': card.get_def_article()
        }
        return render_to_response('ntgreekvocab/fetchcard.html', context, RequestContext(request))

    except SimpleCard.DoesNotExist:
        return HttpResponse("Sorry, card with id " + str(card_id) + " does not exist!")

def ajax_clear_lesson_filters(request):
    if request.is_ajax():
        try:
            del request.session['ln']
            return HttpResponse('Lesson filter cleared.')
        except Error:
            return HttpResponse('Error occurred.')
    else:
        return HttpResponse('Must be ajax request.')