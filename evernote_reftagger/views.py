import sys
import hashlib
import binascii
import time
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

import urllib
import urllib2

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

#
# NOTE: You must change the consumer key and consumer secret to the 
#       key and secret that you received from Evernote
#
consumerKey = "leehsueh"
consumerSecret = "1ca94529bdb70d97"

evernoteHost = "sandbox.evernote.com"
tempCredentialRequestUri = "https://" + evernoteHost + "/oauth"
resOwnerAuthUri = "https://" + evernoteHost + "/OAuth.action"
resEmbeddedParam = "?format=microclip"
resMobileParam = "?format=mobile"
tokRequestUri = tempCredentialRequestUri

userStoreUri = "https://" + evernoteHost + "/edam/user"
noteStoreUriBase = "https://" + evernoteHost + "/edam/note/"

userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
userStore = UserStore.Client(userStoreProtocol)

versionOK = userStore.checkVersion("Python EDAMTest",
                                   UserStoreConstants.EDAM_VERSION_MAJOR,
                                   UserStoreConstants.EDAM_VERSION_MINOR)

def test(request):
    request_params = {}
    request_params['oauth_consumer_key'] = consumerKey
    request_params['oauth_signature'] = consumerSecret
    request_params['oauth_signature_method'] = 'PLAINTEXT'
    request_params['oauth_callback'] = "https://" + request.get_host() + '/evernote/callback'

    timestamp = get_timestamp()
    request_params['oauth_timestamp'] = timestamp

    data = urllib.urlencode(request_params)
    req = urllib2.Request(tempCredentialRequestUri, data)
    response = urllib2.urlopen(req)

    import urlparse
    response_params = urlparse.parse_qs(response.read())
    oauth_token = response_params['oauth_token'][0]
    oauth_callback_confirmed = response_params['oauth_callback_confirmed'][0]

    authUrl = resOwnerAuthUri + "?oauth_token=" + oauth_token
    return HttpResponseRedirect(authUrl)


def oauth_callback(request):
    if request.method == 'GET':
        params = dict(request.GET)
        if 'oauth_token' in params.keys() and 'oauth_verifier' in params.keys():
            oauth_token = request.GET.get('oauth_token')
            oauth_verifier = request.GET.get('oauth_verifier')
            request_params = {}
            request_params['oauth_consumer_key'] = consumerKey
            request_params['oauth_signature'] = consumerSecret
            request_params['oauth_signature_method'] = 'PLAINTEXT'
            request_params['oauth_token'] = oauth_token
            request_params['oauth_verifier'] = oauth_verifier
            request_params['oauth_timestamp'] = get_timestamp()

            data = urllib.urlencode(request_params)
            req = urllib2.Request(tokRequestUri, data)
            response = urllib2.urlopen(req)

            import urlparse
            response_params = urlparse.parse_qs(response.read())
            keys = response_params.keys()
            if 'oauth_token' in keys and 'edam_shard' in keys and 'edam_userId' in keys:
                auth_token = response_params.get('oauth_token')[0]
                edam_shard = response_params.get('edam_shard')[0]
                edam_userId = response_params.get('edam_userId')[0]

                user = userStore.getUser(auth_token)

                noteStoreUri =  noteStoreUriBase + edam_shard
                noteStoreHttpClient = THttpClient.THttpClient(noteStoreUri)
                noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
                noteStore = NoteStore.Client(noteStoreProtocol)

                notebooks = noteStore.listNotebooks(auth_token)
                print "Found ", len(notebooks), " notebooks:"
                for notebook in notebooks:
                    print "  * ", notebook.name
                    if notebook.defaultNotebook:
                        defaultNotebook = notebook
                c = {
                    'notebooks': notebooks,
                    'username': user.username,
                    'auth_token': auth_token,
                    'edam_userId': edam_userId,
                }
                return render_to_response("evernote_reftagger_info.html", c,
                            context_instance=RequestContext(request)))
            else:
                return HttpResponse('Missing oauth_token, edam_shard, or edam_userId')

        else:
            return HttpResponse("Missing request parameters.")
    else:
        return HttpResponse("not a get request..")

def get_timestamp():
    import time
    timestamp = int(round(time.time() * 1000))
    return timestamp

