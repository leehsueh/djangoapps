from siteapps_v1 import settings
from siteapps_v1.bibledb.models import Verse, Category, Entry, Tag, FAQ, UIString, StaticContent, Update
from siteapps_v1.bibledb.forms import BibleVerseForm, EntryForm, VerseListForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.comments import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Max, Min

import string, re

# init code
init = True

def slugify(s):
    remove_list = ['the','and','a']
    s = s.lower().split()
    for word in remove_list:
        while word in s:
            s.remove(word)
    
    for n in range(len(s)):
        word = s[n]
        for c in string.punctuation:
            word.replace(c,'')
        #s[n] = word.translate(string.maketrans('abc','abc'), string.punctuation)
    return '-'.join(s)

def book_slug_to_title(book_slug):
    return book_slug.replace('-',' ').title().replace('Of','of')    # songs-of-solomon -> songs of solomon -> Songs Of Solomon -> Songs of Solomon
    
def refresh_categories(request):
    if settings.PRNT_STMT:
        print 'Refreshing category tree!'
    categories = [] # dict()
    root_cat_list = []
    root_categories = list(Category.objects.filter(parent=None).exclude(category__in=['Uncategorized', 'Pending Categorization']).order_by('category'))
    root_categories = root_categories + list(Category.objects.filter(category__in=['Uncategorized','Pending Categorization']))
    
    try:
        del request.session['categories']
    except KeyError:
        pass
    finally:
        request.session['categories'] = root_categories

def refresh_tags(request):
    if settings.PRNT_STMT:
        print 'Refreshing tags!'
    
    try:
        del request.session['tags']
    except KeyError:
        pass
    finally:
        request.session['tags'] = Tag.objects.annotate(Count('entry')).values('id','slug','name','entry__count').order_by('name')
        maxEm = 2.5
        minEm = 1
        maxEntries = Tag.objects.annotate(num_entries=Count('entry')).aggregate(Max('num_entries'))['num_entries__max']
        minEntries = Tag.objects.annotate(num_entries=Count('entry')).aggregate(Min('num_entries'))['num_entries__min']
        for tag in request.session['tags']:
            tag['weight'] = (tag['entry__count'] +0.0 - minEntries)/maxEntries * maxEm + minEm
            if settings.PRNT_STMT: print tag['weight']

def get_category_tree(request):
    """ get categories as a dictionary """
    global init
    if init or 'categories' not in request.session.keys():
        refresh_categories(request)
        init = False
    return request.session['categories']

def get_tags(request):
    """get tags list"""
    global init
    if init or 'tags' not in request.session.keys():
        refresh_tags(request)
        init = False
    return request.session['tags']

def clear_session(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('bibledb:home'))
        
translations = ["NKJV","NASB","NIV",]
navbar_home = 'Home'
navbar_browse_bible = 'Browse Bible'
navbar_browse_entries = 'Browse Entries'
navbar_add_entry = 'Add Entry'
navbar_add_list = 'Add List'
navbar_faq = 'FAQ'
    
def browse_kjv_context(request):
    """A context processor that provides common information for browsing Bible views:"""
    c = {
        'title': 'Browse KJV Bible',
        'navcurrent': navbar_browse_bible,
    }
    return c

def entries_context(request):
    """A context processor that provides common information for entries"""
    c = {
        'navcurrent': navbar_browse_entries,
        
        #data
        'category_tree' : get_category_tree(request),
        'tag_list': get_tags(request)[:20],
    }
    return c

def common_context(request):
    """A context processor that provides common information"""
    c = {
        'SITE_URL': settings.SITE_URL,
        'webmasteremail': 'admin@tjcbdb.info',
        'translations': translations,
        'navbarItems': [(navbar_home, reverse('bibledb:home')), (navbar_browse_bible, reverse('bibledb:browse-kjv')), (navbar_browse_entries, reverse('bibledb:entries-browse')), (navbar_add_entry, reverse('bibledb:add-entry')), (navbar_add_list, reverse('bibledb:add-list')), (navbar_faq, reverse('bibledb:faq')),],
    }
    return c
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('bibledb:home'))

"""@login_required
def edit_user(request):
    user = request.user
    if request.method == 'POST':
        pd = request.POST
        keys = pd.keys()
        if 'oldPasswd' in keys and 'newPasswd' in keys and 'newPasswd2' in keys:
            if not user.check_password(pd['oldPasswd']):
                return HttpResponse('Incorrect password')
            if pd['newPasswd'] != pd['newPasswd2']:
                return HttpResponse('Passwords do not match')
            
            user.set_password(pd['newPasswd'])
        
        else:
            return HttpResponse('Missing parameters')
    else:
        # display blank form"""
    
# TODO: use to show ALL categories (homepage shows a subset)
# TODO: implement similar view for showing all tags
def browse_categories(request):
    c = {
        'category_dict' :get_category_tree(request),
        'url_prefix': cat_url_prefix,
    }
    return render_to_response('bibledb/category_tree.html', c)

def home(request):
    recent_entries = Entry.objects.all().exclude(removed=True).order_by('-pub_date')[:5]
    recent_comments = Comment.objects.filter(content_type=ContentType.objects.get(model__iexact='Entry')).exclude(is_removed=True).order_by('-submit_date')[:5]
    
    c = {
        'updates': Update.objects.all().order_by('-pub_date')[:1][0],
        'welcomeblurb': StaticContent.objects.get(name__exact='welcome-blurb'),
        'recententries': recent_entries,
        'recentcomments': recent_comments,
        'title': 'Home',
        'navcurrent': navbar_home,
		#'add_entry_form' : EntryForm(),
    }
    return render_to_response('bibledb/base_home.html', c, 
        RequestContext(request, processors=[common_context, entries_context]))

def faq(request):
    c = {
        'faqs': FAQ.objects.all(),
        'title': 'FAQ',
        'faqblurb': StaticContent.objects.get(name__exact='faq-blurb'),
        'navcurrent': navbar_faq,
    }
    return render_to_response('bibledb/faq.html', c, 
        RequestContext(request, processors=[common_context,]))

def display_entries(request, slug='', bookname=None, chpnum=None, type='main'):
    bibleForm = BibleVerseForm()
    entries = []
    term = '**'
    try:
        if type == 'main':
            if request.method == 'GET' and 'book' in request.GET.keys():
                bibleForm = BibleVerseForm(request.GET)
                if bibleForm.is_valid():
                    cd = bibleForm.cleaned_data
                    bookname = cd['book']
                    chpnum = cd['chapter']
                    add_url = [cd['book'].replace(' ','-'), '/']
                    #startverse = cd['startverse']
                    #endverse = cd['endverse']
                    #if startverse: add_url += [str(startverse.verse_ref)]
                    #if endverse: add_url += ['-', str(endverse.verse_ref),'/']
                    if chpnum: 
                        add_url = reverse('bibledb:entries-chapter', kwargs={'bookname':slugify(bookname), 'chpnum':chpnum,})
                    else:
                        add_url = reverse('bibledb:entries-book', kwargs={'bookname':slugify(bookname)})
                    
                    return HttpResponseRedirect(add_url)
                    
            else:
                c = {
                'title': 'Browse Entries',
                'browse_bible_form': bibleForm,
                }
                return render_to_response('bibledb/browse_entries.html', c, RequestContext(request, processors=[common_context, entries_context]))
            
        elif type == 'all':
            term = '(all)'
            entries = Entry.objects.all().exclude(removed=True).order_by('-pub_date').values('id','startverse','endverse','title','pub_date','created_by','num_votes')
                
        elif type == 'passage':
            bookname = book_slug_to_title(bookname)
            entries = Entry.objects.entries_book_chapter_related(bookname, chpnum)
            term = bookname
            if chpnum: term = term + ' ' + str(chpnum)

            initial_data = {'book':bookname, 'chapter':chpnum,}
            bibleForm = BibleVerseForm(initial_data)
            
        elif type == 'category':
            if slug == '':
                c = {
                'title': 'Browse Entries by Category',
                'browse_bible_form': bibleForm,
                'category_list' : True,
                }
                return render_to_response('bibledb/browse_entries.html', c, RequestContext(request, processors=[common_context, entries_context]))
            if not slug == 'uncategorized':
                cat = Category.objects.get(slug=slug)
                term = cat.category
                entries = cat.entry_set.all().exclude(removed=True).values('id','startverse','endverse','title','pub_date','created_by','num_votes')
            else:
                cat = Category.objects.get(slug='uncategorized')
                term = '(uncategorized)'
                entries = cat.entry_set.all().exclude(removed=True).values('id','startverse','endverse','title','pub_date','created_by','num_votes')

        elif type == 'username':
            if slug == '':
                c = {
                'title': 'Browse Entries by User',
                'browse_bible_form': bibleForm,
                'user_list' : User.objects.all().values('id','username'),
                }
                return render_to_response('bibledb/browse_entries.html', c, RequestContext(request, processors=[common_context, entries_context]))
                
            user = User.objects.get(username__iexact=slug)
            entries = Entry.objects.entries_created_by(user)
            term = "user " + user.username
                
        elif type == 'tag':
            no_tags = 'untagged'
            if slug == '':
                c = {
                'title': 'Browse Entries by Tag',
                'browse_bible_form': bibleForm,
                'tag_list_full' : get_tags(request),
                }
                return render_to_response('bibledb/browse_entries.html', c, RequestContext(request, processors=[common_context, entries_context]))
                
            if not slug == no_tags:
                tag = Tag.objects.get(slug=slug)
                term = tag.name
                entries = tag.entry_set.all().order_by('startverse').exclude(removed=True).values('id','startverse','endverse','title','pub_date','created_by','num_votes')
            else:
                entries = Entry.objects.filter(tags=None).order_by('startverse').exclude(removed=True).values('id','startverse','endverse','title','pub_date','created_by','num_votes')
                term = '(' + no_tags.capitalize() + ')'
        else:
            raise Http404("Something is wrong...type is not recognized")
        
        # sort method
        sort = request.GET.get('sort','-pub_date')
        if not re.match('-?(title|pub_date|num_votes|startverse)$',sort):
            sort = '-pub_date'  # default sort by pub_date descending (newest first)
        entries = Entry.objects.make_entry_dicts(entries.order_by(sort))
        
        # get page number from request; default to 1
        paginator = Paginator(entries,10)
        try:
            page = int(request.GET.get('p', '1'))
        except ValueError:
            page = 1
            
        # if page request is out of range, deliver last page
        try:
            entries_page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            entries_page = paginator.page(paginator.num_pages)
            
        c = {
            'title': 'View Entries for ' + term,
            'browse_bible_form': bibleForm,
            'entries': entries,
            'entries_paginator': entries_page,
            'content_header': 'Results for ' + term,
        }
        return render_to_response('bibledb/entry_list.html', c, RequestContext(request, processors=[common_context, entries_context]))
        
    except Category.MultipleObjectsReturned:
        raise Http404("Uh oh; multiple categories returned for given slug " + slug + "! If you got here by clicking on a link, please inform the webmaster of this error and how you got to it!")
    except Category.DoesNotExist:
        raise Http404("No category with slug " + slug + " exists.")
    except Tag.MultipleObjectsReturned:
        raise Http404("Uh oh; multiple tags returned for given slug " + catslug + "! If you got here by clicking on a link, please inform the webmaster of this error and how you got to it!")
    except Tag.DoesNotExist:
        raise Http404("No tag with slug " + slug + " exists.")

    
def display_entry(request, entry_id):
    """ Display detailed information on single Entry record """
    try:
        e = Entry.objects.get(id=entry_id, removed__in=[None, False])
        error_message = None
        related_entries_passage = Entry.objects.entries_passage_related(e.startverse, e.endverse, e.id)
        related_entries_category = e.related_entries_category()
        related_entries_tag = e.related_entries_tag()
        
        # only get necessary information for related entries
        related_entries_passage = Entry.objects.make_entry_dicts(related_entries_passage)
        related_entries_category = Entry.objects.make_entry_dicts(related_entries_category)
        related_entries_tag = Entry.objects.make_entry_dicts(related_entries_tag)
        
        if request.method == 'POST':
            # add more tags
            if 'additional_tags' in request.POST.keys() and request.POST['additional_tags']:
                more_tags = request.POST['additional_tags'].split(',')
                for tag in more_tags:
                    tag = tag.strip()
                    test = Tag.objects.filter(name__iexact=tag)
                    if len(test) == 0:
                        new_tag = Tag(name=tag,slug=slugify(tag))
                        new_tag.save()
                        e.tags.add(new_tag)
                    elif test[0] not in e.tags.all():
                        e.tags.add(test[0])
                e.save()
                refresh_tags(request)
            # add a vote
            elif 'addVote' in request.POST.keys():
                if str(entry_id) not in request.session.keys():
                    # increment the vote count for this entry and save
                    request.session[str(entry_id)] = True
                    e.num_votes = e.num_votes + 1
                    e.save()
                    
                else: error_message = 'You already voted.'
    
        passage = Verse.objects.get_passage(e.startverse, e.endverse)
        if len(passage) > 1:
            passage_ref = ''.join([str(passage[0]), '-', str(passage[len(passage)-1].verse_ref)])
        else:
            passage_ref = str(passage[0])
        c = {
            'title': 'Entry: ' + e.title + ' (' + passage_ref + ')',
            'error_message': error_message,
            'entry': e,
            'edit_text': 'Edit Entry',
            'delete_text': 'Delete',
            'verse_list': passage,
            'passage_ref': passage_ref,
            'related_entries_passage': related_entries_passage,
            'related_entries_category': related_entries_category,
            'related_entries_tag': related_entries_tag,
            # user object is available if using RequestContext
            #'user_authenticated': request.user.is_authenticated(),
            #'user': request.user,
        }
        return render_to_response('bibledb/entry_detail.html', c, RequestContext(request, processors=[common_context, entries_context]))
    except Entry.DoesNotExist:
        raise Http404("Sorry, entry with id " + str(entry_id) + " does not exist!")

add_entry_name = 'addEntry'
add_entry_header = 'Add Verse/Passage'
add_verse_list_name = 'addVerseList'
add_verse_list_header = 'Add a Verse List'

@login_required        
def add_content(request, type):
    """ type parameter (either verse_list or entry) only used for rendering the correct blank form """
    if request.method == 'POST':
        post_keys = request.POST.keys()
        if add_entry_name in post_keys:
            form = EntryForm(request.POST)
            navCurrent = navbar_add_entry
            if form.is_valid():
                e = Entry()
                cd = form.cleaned_data
                
                bookname = cd['book'].title().replace('Of','of')
                chapter = cd['chapter']
                #return HttpResponse(cd['startverse'])
                startverse = cd['startverse']
                endverse = cd['endverse']
                """startverse = get_object_or_404(Verse, book=bookname, chapter_ref=chapter, verse_ref=cd['startverse'])
                if cd['endverse']:
                    endverse = get_object_or_404(Verse, book=bookname, chapter_ref=chapter, verse_ref=cd['endverse'])
                else:
                    endverse = None"""

                # e_tags = list(cd['tags'])
                e_tags = []
                
                if cd['additional_tags']:
                    more_tags = cd['additional_tags'].split(',')
                    for tag in more_tags:
                        tag = tag.strip()
                        test = Tag.objects.filter(name__iexact=tag)
                        if len(test) == 0:
                            new_tag = Tag(name=tag,slug=slugify(tag))
                            new_tag.save()
                            e_tags.append(new_tag)
                        elif test[0] not in e_tags:
                            e_tags.append(test[0])
                
                e.startverse = startverse
                e.endverse = endverse
                e.title = cd['title']
                e.context_notes = cd['context_notes']
                e.notes = cd['notes']
                e.created_by = request.user
                e.save()
                e.categories = cd['categories']
                e.tags = e_tags
                e.save()
                refresh_tags(request)
                
                # TODO: make this url thing better
                return HttpResponseRedirect(reverse('bibledb:entry-view',kwargs={'entry_id': e.id}))# + '/entry/' + str(e.id))
            else:
                form_submit_name = add_entry_name
                form_header = add_entry_header
                
        elif add_verse_list_name in post_keys:
            form = VerseListForm(request.POST)
            navCurrent = navbar_add_list
            if form.is_valid():
                cd = form.cleaned_data
                vl = Category(category=cd['category'], parent=cd['parent'], slug=slugify(cd['category']), created_by=request.user)
                vl.save()
                refresh_categories(request)
                return HttpResponseRedirect(reverse('bibledb:home'))
            else:
                form_submit_name = add_verse_list_name
                form_header = add_verse_list_header
        else:
            return HttpResponse("Hello, how did you get here??")
            
    else: # not a post request
        if type == 'entry': 
            form = EntryForm()
            form_submit_name = add_entry_name
            form_header = add_entry_header
            static_explanation = StaticContent.objects.get(name='entry-explanation').content
            navCurrent = navbar_add_entry
        elif type == 'verse_list': 
            form = VerseListForm()
            form_submit_name = add_verse_list_name
            form_header = add_verse_list_header
            static_explanation = StaticContent.objects.get(name='category-explanation').content
            navCurrent = navbar_add_list

    c = {
        'title': 'Add Content',
        'static_explanation': static_explanation,
        'navcurrent': navCurrent,
        'form': form,
        'form_header': form_header,
        'form_submit_name': form_submit_name,
    }
    return render_to_response('bibledb/add_form.html', c, RequestContext(request, processors=[common_context, entries_context]))

@login_required
def remove_entry(request, entry_id):
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        raise Http404("Sorry, entry with id " + str(entry_id) + " does not exist!")
        
    if request.user == entry.created_by:
        if request.GET.get('a','') == 'undo':
            entry.removed = False
            entry.save()
            return HttpResponseRedirect(reverse('bibledb:entry-view', kwargs={'entry_id':entry.id}))
        else:
            entry.removed = True
            entry.save()
            return HttpResponse('Entry successfully removed. <a href="' + reverse('bibledb:entry-remove',kwargs={'entry_id': entry.id}) + '?a=undo">Undo</a>, or go <a href="' + reverse('bibledb:home') + '">home</a>')
    else:
        return HttpResponse('Sorry, you do not have permission to do this action.')

@login_required
def edit_entry(request, entry_id):
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        raise Http404("Sorry, entry with id " + str(entry_id) + " does not exist!")
    
    # check if user is the one who created the entry
    if request.user == entry.created_by:
        if request.method == 'POST' and 'editEntry' in request.POST.keys():
            if request.POST['editEntry'] == 'Cancel':
                return HttpResponseRedirect(reverse('bibledb:entry-view', kwargs={'entry_id':entry.id}))
            
            form = EntryForm(request.POST)
            if form.is_valid():
                try:
                    cd = form.cleaned_data
                    entry.startverse = cd['startverse']
                    entry.endverse = cd['endverse']
                    entry.title = cd['title'] #request.POST['title']
                    entry.context_notes = cd['context_notes'] #request.POST['context_notes']
                    entry.notes = cd['notes'] #request.POST['notes']
                    entry.categories = cd['categories']
                    entry.save()
                    
                    return HttpResponseRedirect(reverse('bibledb:entry-view', kwargs={'entry_id':entry.id}))
                except KeyError:
                    raise Http404("Invalid POST or form parameters")
        else:
            initial_data = {
                'book': entry.startverse.book,
                'chapter': entry.startverse.chapter_ref,
                'startverse': entry.startverse.verse_ref,
                'title': entry.title,
                'context_notes': entry.context_notes,
                'notes': entry.notes,
                'categories': entry.categories,
            }
            if entry.endverse:
                initial_data['endverse'] = entry.endverse.verse_ref
            form = EntryForm(initial_data)
            
        c = {
            'title': 'Edit Entry',
            'can_edit': True,
            'form': form,
            'form_header': 'Edit Entry',
            'form_submit_name': 'editEntry',
            'categories': entry.categories.all(),
        }
        return render_to_response('bibledb/edit_entry.html', c, 
            RequestContext(request, processors=[common_context, entries_context]))
        return HttpResponse('You edited this entry! %s' % entry.created_by)
    else:
        return HttpResponse('Sorry, you do not have permission to edit this entry.')
    
# Below views deal with browsing the Bible ####
def browse_kjv(request):
    """display a form with book, chapters, and verses fields"""
    books = Verse.objects.get_all_books()
    if request.method == 'GET' and 'book' in request.GET.keys():
        form = BibleVerseForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            
            # TODO: use reverse url look up instead of coupling url scheme in the view
            add_url = [cd['book'].lower().replace(' ','-'), '/']
            chpnum = cd['chapter']
            startverse = cd['startverse']
            endverse = cd['endverse']
            
            if chpnum: add_url +=[str(chpnum),'/']
            if startverse: add_url += [str(startverse.verse_ref)]
            if endverse: add_url += ['-', str(endverse.verse_ref),'/']
            add_url = reverse('bibledb:browse-kjv') + ''.join(add_url)
            
            return HttpResponseRedirect(add_url)
    else:
        form = BibleVerseForm()
    
    return render_to_response('bibledb/browse_bible.html',
                {'title': 'Browse KJV Bible',
                 'browse_bible_form': form,
                 'books': books,
                 'content_header': 'Browse Books',},
                 RequestContext(request, processors=[common_context, browse_kjv_context])
            )

def display_chapters(request, bookname):
    """displays a list of chapters for the given book"""
    book_slug = bookname
    bookname = book_slug_to_title(bookname)
    related_entries = Entry.objects.entries_book_chapter_related(bookname, None)
    limit = 10
    chp_count = Verse.objects.validate_book(bookname)
    if not chp_count:
        raise Http404('Book does not exist. Check your spelling?')
        
    chp_range = range(1,chp_count+1)
    return render_to_response('bibledb/browse_bible.html', { 
            'bookname': bookname,
            'relatedentriesbook': Entry.objects.make_entry_dicts(related_entries[:limit]),
            'chprange': chp_range,
            'browse_bible_form': BibleVerseForm({'book': bookname,}),
            'content_header': 'Chapters in ' + bookname,
        }, RequestContext(request, processors=[common_context, browse_kjv_context]))
        
def display_verses(request, bookname, chpnum, startverse=None, endverse=None):
    """ displays verses """
    book_slug = bookname
    bookname = book_slug_to_title(bookname)
    related_entries_book = Entry.objects.entries_book_chapter_related(bookname, None)
    related_entries_chp = Entry.objects.entries_book_chapter_related(bookname, chpnum)
    limit = 10
    
    # TODO: add validation checks
    if not Verse.objects.validate_chapter(bookname, chpnum):
        raise Http404('Invalid chapter for book: %s' % (bookname))
    
    # print all verses in chapter
    if (not startverse) and (not endverse):
        verses = Verse.objects.filter(book=bookname, chapter_ref=chpnum).order_by('id')
        passage_ref = ' '.join([bookname, str(chpnum)])
        
    # print single verse
    elif startverse and (not endverse):
        if not Verse.objects.validate_verse(bookname, chpnum, startverse):
            raise Http404('Invalid verse')
        verses = Verse.objects.filter(book=bookname, chapter_ref=chpnum, verse_ref=startverse)
        passage_ref = ' '.join([str(verses[0]),])
        
    # print verses in range
    else:
        start_verse = get_object_or_404(Verse, book=bookname, chapter_ref=chpnum, verse_ref=startverse)
        end_verse = get_object_or_404(Verse, book=bookname, chapter_ref=chpnum, verse_ref=endverse)
        #num_verses = Verse.objects.num_verses_in_range(start_verse, end_verse)
        verses = Verse.objects.get_passage(start_verse, end_verse)
        passage_ref = ' '.join([str(verses[0]), '-', str(verses[len(verses)-1].verse_ref)])
    
    chp_count = Verse.objects.validate_book(bookname)
    if not chp_count:
        raise Http404('Book does not exist. Check your spelling?')
        
    chp_range = range(1,chp_count+1)

    return render_to_response('bibledb/browse_bible.html', {
            'verse_list': verses,
            'content_header': passage_ref,
            'nextchapter': Verse.objects.get_next_chapter(verses[0]),
            'prevchapter': Verse.objects.get_previous_chapter(verses[0]),
            'bookname': bookname,
            'chprange': chp_range,
            'browse_bible_form': BibleVerseForm({
                'book': bookname,
                'chapter': chpnum,
                'startverse': startverse,
                'endverse': endverse,}),
            'relatedentriesbook': Entry.objects.make_entry_dicts(related_entries_book[:limit]),
            'relatedentrieschp': Entry.objects.make_entry_dicts(related_entries_chp[:limit]),
        }, RequestContext(request, processors=[common_context, browse_kjv_context]))
        
def ajax_passage(request, bookname, chpnum, startverse, endverse=None):
    """NOTE: all parameters are passed in as strings"""
    
    bookname = book_slug_to_title(bookname)
    if not endverse: endverse = startverse
    
    if settings.PRNT_STMT: 
        print bookname, chpnum, startverse, endverse
        
    if int(startverse) > int(endverse):
        return HttpResponse('End verse must be greater than start verse.')
    if not Verse.objects.validate_chapter(bookname, chpnum):
        return HttpResponse('Invalid chapter %s for book: %s' % (str(chpnum),bookname))
    if not Verse.objects.validate_verse(bookname, chpnum, startverse) or not Verse.objects.validate_verse(bookname,chpnum,endverse):
        return HttpResponse('Invalid verse(s)')
    
    
    max_verses = 10
    
    passage = Verse.objects.filter(
        book__iexact=bookname,  \
        chapter_ref=chpnum, \
        verse_ref__gte=min(int(startverse),int(endverse)),    \
        verse_ref__lte=max(int(startverse),int(endverse)) \
        ).order_by('verse_ref').values('verse_ref','verse_text')

    return render_to_response('bibledb/ajax_passage.html', {
        'passage': passage,
        'bookname': bookname,
        'chpnum': chpnum,
        'startverse':startverse,
        'endverse':endverse,
    }, RequestContext(request))