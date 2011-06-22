from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.mail import send_mail
import urllib
import urllib2
from django.utils import simplejson

# Create your views here.
def hub(request):
    return render_to_response('hub.html', {})

def ajax_contactable(request):
    if request.is_ajax():
        try:
            name = request.GET['name']
            email = request.GET['email']
            comment = request.GET['comment']
            subject = request.GET['subject']
            message = u"Message: " + comment + u"\nFrom " + name + u"\nReply to " + email
            send_mail(subject, message, email, ['leehsueh7@gmail.com',], fail_silently=False)
            return HttpResponse(u'success')
        except Error:
            return HttpResponse(u'Error trying to send message. Please email admin@tjcbdb.info.')
    else:
        return HttpResponse(u'Invalid')

def janrain_token_url(request):
    params = dict(request.POST)
    token = params['token'][0]
    api_key = "d8cd96a5b5372c15e235211eac81059c6b4df50c"
    api_params = {
        'token': token,
        'apiKey': api_key,
        'format': 'json',   
    }
    # make the api call
    http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info',
                            urllib.urlencode(api_params))
    
    # read json response
    auth_info_json = http_respnse.read()
    auth_info = simplejson.loads(auth_info_json)
    if auth_info['stat'] == 'ok':
        profile = auth_info['profile']
        
        # identifier is the unique identifier used to sign user into site
        identifier = profile['identifier']

        # these fields MAY be in the profile, but are not guaranteed. it
        # depends on the provider and their implementation.
        name = profile.get('displayName')
        email = profile.get('email')

        # TODO: sign user in with custom backend

        return HttpResponse(identifier + '\n' + name
            + '\n' + email)
