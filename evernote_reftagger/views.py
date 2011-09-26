from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors
import evernote.edam.limits.constants as Constants

from siteapps_v1.evernote_oauth.views import parse_oauth_credentials, redirect_oauth_start, get_user_store, get_note_store, get_user_and_note_stores, unhandled_edam_user_exception
from siteapps_v1.evernote_oauth.views import EVERNOTE_OAUTH_TOKEN, EVERNOTE_EDAM_SHARD, EVERNOTE_EDAM_USERID
import urllib

def list_notes(request):
    if request.session.get(EVERNOTE_OAUTH_TOKEN, False) and request.session.get(EVERNOTE_EDAM_SHARD, False) and request.session.get(EVERNOTE_EDAM_USERID, False):
        auth_token = request.session.get(EVERNOTE_OAUTH_TOKEN)
        edam_shard = request.session.get(EVERNOTE_EDAM_SHARD)
        edam_userId = request.session.get(EVERNOTE_EDAM_USERID)

        try:
            userStore, noteStore = get_user_and_note_stores(edam_shard)

            user = userStore.getUser(auth_token)
            notebooks = noteStore.listNotebooks(auth_token)
            for notebook in notebooks:
                if notebook.defaultNotebook:
                    defaultNotebook = notebook
            
            # get notes in default notebook
            filter = NoteStore.NoteFilter()
            filter.notebookGuid = defaultNotebook.guid
            note_list = noteStore.findNotes(auth_token, filter, 0, 5)
            notes = []
            for note in note_list.notes:
                notes.append({
                    'title': note.title, 
                    'content': noteStore.getNoteContent(auth_token, note.guid),
                })
                
            c = {
                'notebooks': notebooks,
                'username': user.username,
                'edam_userId': edam_userId,
                'notes': notes,
            }
            return render_to_response("evernote_reftagger_info.html", c,
                        context_instance=RequestContext(request))
        except Errors.EDAMUserException as e:
            if e.errorCode == Errors.EDAMErrorCode.AUTH_EXPIRED:
                # authentication token expired; re-initiate oauth process
                return redirect_oauth_start(request)
            else:
                return unhandled_edam_user_exception(e)
    else:
        # request is either a callback invoked by evernote, or invoked by user to initiate evernote oauth
        credentials = parse_oauth_credentials(request)
        if credentials:
            # authentication has been done; callback invoked by Evernote
            # values stored in session
            return HttpResponseRedirect(request.build_absolute_uri(request.path))
        else:
            # authentication has not been done; initiate oauth process
            return redirect_oauth_start(request)

def public_notebook(request, username, uri):
    # if request.GET.get('publicUrl', False):
    #    return HttpResponse("URI no specified")
    # notebook_uri = request.GET['publicUrl']
    # import re

    # # parse the uri for a username
    # first = notebook_uri.find('/pub/')
    # if first == -1:
    #     return HttpResponse('Invalid notebook URI:' + notebook_uri)
    # last = notebook_uri.find('/', first + 5)
    # if last == -1:
    #     return HttpResponse('Invalid notebook URI:' + notebook_uri)
    # username = notebook_uri[first + 5:last]
    # uri = notebook_uri[last+1:]
    # if uri[-1] == '/':
    #     uri = uri[:-1]
    
    userStore = get_user_store()
    try:
        user = userStore.getPublicUserInfo(username)
        user_id = user.userId
        shard_id = user.shardId
    except Errors.EDAMUserException as e:
        return unhandled_edam_user_exception(e)

    try:
        noteStore = get_note_store(shard_id)
        notebook = noteStore.getPublicNotebook(user_id, uri)
    except Errors.EDAMNotFoundException as e:
        return HttpResponse("Notebook not found for user " + username + " and notebook uri " + uri)

    filter = NoteStore.NoteFilter()
    filter.notebookGuid = notebook.guid
    note_list = noteStore.findNotes('', filter, 0, Constants.EDAM_USER_NOTES_MAX)
    c = {
        'notebook': notebook,
        'notes': note_list.notes,
        'user': user,
    }
    return render_to_response('evernote_reftagger_public_notebook.html', c,
        context_instance=RequestContext(request))

def fetch_public_note(request, username, uri, note_guid):
    userStore = get_user_store()
    try:
        user = userStore.getPublicUserInfo(username)
        user_id = user.userId
        shard_id = user.shardId
    except Errors.EDAMUserException as e:
        return unhandled_edam_user_exception(e)
        
    noteStore = get_note_store(shard_id)
    note = noteStore.getNote(
        '',
        note_guid,
        True,
        False,
        False,
        False
        )
    c = {
        'note': note
    }
    return render_to_response('evernote_reftagger_note.html', c,
        context_instance=RequestContext(request))