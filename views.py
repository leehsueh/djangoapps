from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.
def hub(request):
    return render_to_response('hub.html', {})

def env_info(request):
    import sys
    import django
    return HttpResponse(sys.version + '<br>' + django.get_version())

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