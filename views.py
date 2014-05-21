# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from map.models import *
from django.template import RequestContext

from account.models import Author

from django.contrib.auth.decorators import login_required

#@login_required
def home(request, uid=None):
    request.session['human'] = True;
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    obj = None
    uid = uid or request.GET.get('uid')
    if uid:
        id, t = uid.split('-')
        if t == 't':
            M = Track
        else:
            M = Point
        qs = M.objects.filter(uid=uid)
        if qs.count() != 0:
            obj = qs[0]
    types = Type.objects.all()
    for t in types:
        t.acl = acl
    return render_to_response('home_new.html',
                              {'tracks': Track.objects.filter(state__lte=acl),
                               'types': types,
                               'rovar_uid': uid,
                               'obj': obj,
                               'authors': Author.objects.all(),
                               },
                              context_instance=RequestContext(request))

#@login_required
def info(request):
    return render_to_response('info.html',
                              {'authors': Author.objects.all(),
                               'show_left_panel': not request.GET.get('blank')},
                              context_instance=RequestContext(request))
    

#from django.utils.http import is_safe_url
from django.utils.translation import activate

def set_language(request):
    next = request.REQUEST.get('next')
    #if not is_safe_url(url=next, host=request.get_host()):
    next = request.META.get('HTTP_REFERER')
    #if not is_safe_url(url=next, host=request.get_host()):
    #        next = '/'
    response = HttpResponseRedirect(next)
    if request.method == 'GET':
        lang_code = request.GET.get('language', None)
        if lang_code:
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response
