# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext
from django.utils import translation
import os
import re

from account.models import Author
from map.models import *

from django.contrib.auth.decorators import login_required

#@login_required
def home(request, uid=None, slug=None):
    request.session['human'] = True;
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    obj = None
    uid = uid or request.GET.get('uid')
    if uid:
        if re.match('^\d+\-[pt]$', uid):
            id, t = uid.split('-')
            if t == 't':
                M = Track
            else:
                M = Point
            qs = M.objects.filter(id=id)
            if qs.count() != 0:
                obj = qs[0]
        else:
            qs = Track.objects.filter(uid=uid)
            if qs.count() != 0:
                obj = qs[0]
            else:
                qs = Point.objects.filter(uid=uid)
                if qs.count() != 0:
                    obj = qs[0]
                else:
                    return HttpResponseRedirect('/')
            
    types = Type.objects.all()
    #for t in types:
    #    t.acl = acl
        
    template_name = 'info/content-%s.html' % translation.get_language()
    if not os.path.exists(os.path.join(settings.TEMPLATE_DIRS[0], template_name)):
        template_name = 'info-content.html'
    if obj is not None and obj.location:
        l_name = obj.location.name
    else:
        l_name = request.session.get('location', u'Минск')
    
    return render_to_response('home_new.html',
                              {#'tracks': Track.objects.filter(state__lte=acl),
                                  'types': types,
                                  #'rovar_uid': uid,
                                  'obj': obj,
                                  'authors': Author.objects.all(),
                                  'template_name': template_name,
                                  'location': l_name,
                                  'locations': Location.objects.all().values_list("name", flat=True)
                               },
                              context_instance=RequestContext(request))

#@login_required
def info(request):
    template_name = 'info/content-%s.html' % translation.get_language()
    if not os.path.exists(os.path.join(settings.TEMPLATE_DIRS[0], template_name)):
        template_name = 'info-content.html'
    return render_to_response('info.html',
                              {'authors': Author.objects.all(),
                               'show_left_panel': not request.GET.get('blank'),
                               'template_name': template_name},
                              context_instance=RequestContext(request))
    

#from django.utils.http import is_safe_url
from django.utils.translation import activate

def set_language(request):
    next = request.REQUEST.get('next')
    #if not is_safe_url(url=next, host=request.get_host()):
    next = request.META.get('HTTP_REFERER', '/')
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

def set_location(request):
    next = request.REQUEST.get('next')
    next = request.META.get('HTTP_REFERER', '/')
    response = HttpResponseRedirect(next)
    request.session['location'] = request.GET.get('name', 'Minsk')
    return response
    
