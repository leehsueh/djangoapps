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
        try:
            del request.session['ln']
        except KeyError:
            pass
        
    card_ids = cards.values_list('id', flat=True)
    return random.sample(card_ids, num)

def get_lesson_numbers():
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
    return lesson_nums

def common_context(request):
    """context processor for common information for all templates"""
    c = {
        'lessons': get_lesson_numbers(),
    }
    return c

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
        
    return render_to_response('ntgreek_home.html', c, RequestContext(request,
                                                processors=[common_context,]))
def card_random_view(request, card_id):
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

        return render_to_response('ntgreek_home.html', context, RequestContext(request,
                                                processors=[common_context,]))

    except SimpleCard.DoesNotExist:
        raise Http404("Sorry, card with id " + str(card_id) + " does not exist!")

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
    return render_to_response('ntgreek_editcard.html', context, RequestContext(request,
                                                processors=[common_context,]))

@login_required
def card_add(request):
    if request.method == 'POST':
        form = SimpleCardAdminForm(request.POST)
        if form.is_valid():
            cleandata = form.cleaned_data
            # @type card SimpleCard
            card = SimpleCard()
            card.greek_word = cleandata['greek_word']
            card.definition = cleandata['definition']
            card.lesson_number = cleandata['lesson_number']
            card.notes = cleandata['notes']
            card.hints = cleandata['hints']
            card.parsing_info = cleandata['parsing_info']
            card.part_of_speech = cleandata['part_of_speech']
            card.save() # create primary key before saving many to many relationship
            card.related_cards = cleandata['related_cards']
            card.save()
            return HttpResponseRedirect(reverse('ntgreekvocab:card-view', kwargs={'card_id':card.id}))
    else:
        form = SimpleCardAdminForm()

    context = {
        'form': form,
    }
    return render_to_response('ntgreek_editcard.html', context, RequestContext(request,
                                                processors=[common_context,]))

def card_view(request, card_id):
    try:
        card = SimpleCard.objects.get(id=card_id)
        lesson_num = card.lesson_number
        cards_in_lesson = SimpleCard.objects.filter(
                            lesson_number=lesson_num
                        ).order_by(
                            "greek_word"
                        ).values_list(
                            "id","greek_word"
                        )
        # find which index word occurs in alphabetical list within the lesson
        # index used for cross linking on the lesson slider page
        for i in range(0,len(cards_in_lesson)):
            if card.greek_word == cards_in_lesson[i][1]:
                num = i + 1

        if lesson_num == '' or not lesson_num:
            lesson_num = 0
        return HttpResponseRedirect(reverse(
                    'ntgreekvocab:lesson', kwargs={'lesson_num':lesson_num}
                ) + '#' + str(num))

    except SimpleCard.DoesNotExist:
        raise Http404("Sorry, card with id " + str(card_id) + " does not exist!")

def card_list(request):
    words_by_letter = []
    total_fetched = 0
    for letter in greek.alphabet.lc_letters:
        letter_qs = SimpleCard.objects.filter(greek_word__istartswith=letter).order_by('greek_word').values('id','greek_word','definition','lesson_number','part_of_speech')
        total_fetched += letter_qs.count()
        words_by_letter.append((letter, letter_qs))

    parts_of_speech = [(short,long) for short, long in siteapps_v1.ntgreekvocab.models.PARTS_OF_SPEECH_MAP.items()]
    context = {
        'total_fetched': total_fetched,
        'total_words': SimpleCard.objects.all().count(),
        'letters': greek.alphabet.lc_letters,
        'words_by_letter': words_by_letter,
        'parts_of_speech': sorted(parts_of_speech)
    }
    return render_to_response('ntgreek_listcards.html', context, RequestContext(request,
                                                processors=[common_context,]))

def cards_by_lesson(request, lesson_num):
    try:
        if lesson_num == '0' or lesson_num == 'NA':
            # words not associated with a lesson
            lesson_num = '(None)'
            cards = SimpleCard.objects.filter(lesson_number='') | SimpleCard.objects.filter(lesson_number__isnull=True)
        else:
            cards = SimpleCard.objects.filter(lesson_number__iexact=lesson_num)

        if cards.count() == 0:
            raise Http404(u'No words for lesson ' + lesson_num + '.')
            
        context = {
            'cards': cards,
            'lesson_number': lesson_num,
        }
        return render_to_response('ntgreek_lesson_slider.html', context, RequestContext(request,
                                                processors=[common_context,]))
    except:
        return HttpResponseRedirect(reverse('ntgreekvocab:cards-list'))

def card_lookup(request):
    context = {}
    return render_to_response('ntgreek_lookupcard.html', context, RequestContext(request,
                                                processors=[common_context,]))

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
                if request.GET.has_key(u'id') and request.GET[u'id']:
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
        return render_to_response('ntgreek_fetchcard.html', context, RequestContext(request))

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