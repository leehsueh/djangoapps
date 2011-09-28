import sys
import time
import urllib
import urllib2
import urlparse

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from siteapps_v1.google_oauth.views import oauth_start, get_client, clear_google_oauth_session
from siteapps_v1.google_oauth.views import GOOGLE_OAUTH_REQ_TOKEN, GOOGLE_OAUTH_TOKEN

import gdata.gauth
import gdata.docs.client


def get_folder_list(request):
    """Test callback view"""
    if request.session.get(GOOGLE_OAUTH_TOKEN, False):
        client = get_client(
            request.session[GOOGLE_OAUTH_TOKEN].token,
            request.session[GOOGLE_OAUTH_TOKEN].token_secret,
        )
        feed = client.GetDocList(uri='/feeds/default/private/full/-/folder')
        c = {
            'feed': feed,
        }
        return render_to_response("google_reftagger_folder_list.html", c,
                    context_instance=RequestContext(request))

    elif request.session.get(GOOGLE_OAUTH_REQ_TOKEN, False):
        oauth_get_access_token(request)
        return HttpResponseRedirect("http://" + request.get_host() + request.path)
    else:
        return oauth_start(request)

def get_folder_contents(request, resource_id):
    if request.session.get(GOOGLE_OAUTH_TOKEN, False):
        client = get_client(
            request.session[GOOGLE_OAUTH_TOKEN].token,
            request.session[GOOGLE_OAUTH_TOKEN].token_secret,
        )
        folder = client.GetDoc(resource_id)
        feed = client.GetDocList(uri=folder.content.src + "/-/document")  

        c = {
            'folder': folder,
            'feed': feed,
        }
        return render_to_response("google_reftagger_folder.html", c,
                    context_instance=RequestContext(request))

    elif request.session.get(GOOGLE_OAUTH_REQ_TOKEN, False):
        oauth_get_access_token(request)
        return HttpResponseRedirect("http://" + request.get_host() + request.path)

    else:
        return oauth_start(request)

def get_doc_content(request, resource_id):
    if request.session.get(GOOGLE_OAUTH_TOKEN, False):
        client = get_client(
            request.session[GOOGLE_OAUTH_TOKEN].token,
            request.session[GOOGLE_OAUTH_TOKEN].token_secret,
        )
        doc = client.GetDoc(resource_id)
        content = client.GetFileContent(
            uri=doc.content.src + "&exportFormat=html"    
        )
        css_begin_index = content.find('<style type="text/css">')
        css_end_index = content.find('</head>', css_begin_index)
        css_style = content[css_begin_index:css_end_index]
        body_begin = content.find('<body')
        body_end = content.find('</html>')
        body = content[body_begin:body_end]
        c = {
            'doc': doc,
            'style': css_style,
            'body': body
        }
        return render_to_response("google_reftagger_doc.html", c,
                    context_instance=RequestContext(request))

    elif request.session.get(GOOGLE_OAUTH_REQ_TOKEN, False):
        oauth_get_access_token(request)
        return HttpResponseRedirect("http://" + request.get_host() + request.path)

    else:
        return oauth_start(request)
