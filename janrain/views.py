from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404

import urllib, urllib2, json

def test(request):
	return HttpResponse('Hello world')

@csrf_exempt
def login(request):
	if request.method == 'GET':
		if 'next' in request.GET.keys():
			next = request.GET['next']
		else:
			next = '/'
		form = AuthenticationForm()
		context = {
			'next': next,
			'form': form
		}
		return render_to_response(
	        'janrain_login.html',
	        context,
	        context_instance=RequestContext(request)
	    )
	elif request.method == 'POST':
		token = request.POST['token']
		destination = request.POST.get('next', '/tidbits/')

		api_key = settings.JANRAIN_API_KEY

		api_params = {
	        'token': token,
	        'apiKey': api_key,
	        'format': 'json',   
	    }

	    # make the api call
		http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info',
	                            urllib.urlencode(api_params))

	    # read json response
		auth_info_json = http_response.read()
		auth_info = json.loads(auth_info_json)
		if auth_info['stat'] == 'ok':
			profile = auth_info['profile']

			# identifier is the unique identifier used to sign user into site
			identifier = profile['identifier']

			# these fields MAY be in the profile, but are not guaranteed. it
			# depends on the provider and their implementation.
			name = profile.get('displayName')

			# TODO: sign user in with custom backend
			user = auth.authenticate(profile=profile)
			auth.login(request, user)
			return HttpResponseRedirect(destination)
		else:
			return HttpResponse("An error occurred: " + auth_info['err']['msg'])

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('tidbits:home'))