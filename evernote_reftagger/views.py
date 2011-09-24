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
    import pdb; pdb.set_trace()

    import time
    timestamp = int(round(time.time() * 1000))
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
    import pdb; pdb.set_trace()
    if request.method == 'GET':
        oauth_token = request.GET.get('oauth_token')
        oauth_verifier = request.GET.get('oauth_verifier')
        return HttpResponse(oauth_token + "<br>" + oauth_verifier)
    else:
        return HttpResponse("not a get request..")

# user = authResult.user
# authToken = authResult.authenticationToken
# print "Authentication was successful for ", user.username
# print "Authentication token = ", authToken

# noteStoreUri =  noteStoreUriBase + user.shardId
# noteStoreHttpClient = THttpClient.THttpClient(noteStoreUri)
# noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
# noteStore = NoteStore.Client(noteStoreProtocol)

# notebooks = noteStore.listNotebooks(authToken)
# print "Found ", len(notebooks), " notebooks:"
# for notebook in notebooks:
#     print "  * ", notebook.name
#     if notebook.defaultNotebook:
#         defaultNotebook = notebook

