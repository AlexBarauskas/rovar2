from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

def home(request):
    return render_to_response('home.html',
                              {})
    #return HttpResponse('Project run!')
