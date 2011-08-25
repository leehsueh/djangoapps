""" Usage: 
# Module that abstracts the Biblia web service API
"""
import urllib
import urllib2
import json

API_BASE_URL = 'http://api.biblia.com/v1/bible/'
from settings import BIBLIA_API_KEY as API_KEY

def content(bible, ext='txt', request_params={'passage':'John 3:16'}):
    url_path = 'content/' + bible + '.' + ext
    return api_call(url_path, request_params)

def api_call(url_path, request_params):
    request_params['key'] = API_KEY
    data = urllib.urlencode(request_params)
    url = API_BASE_URL + url_path
    result = {}
    try:
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result['success'] = True
        result['response'] = response.read()
        return result
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            result['success'] = False
            result['response'] = e.reason
        elif hasattr(e, 'code'):
            result['success'] = False
            result['response'] = str(e.code)
    else:
        result['success'] = False
        result['response'] = 'Error: ' + e.message
    finally:
        return result