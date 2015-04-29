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
from api.utils import make_api_doc

from django.contrib.auth.decorators import login_required

def short_home(request):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    l_name = request.GET.get('location', u'Minsk')
    try:
        location = Location.objects.get(name=l_name)
    except Location.DoesNotExist:
        try:
            location = Location.objects.filter(default=True)[0]
        except:
            location = Location.objects.all()[0]
    template_name = 'info/content-%s.html' % translation.get_language()
    if not os.path.exists(os.path.join(settings.TEMPLATE_DIRS[0], template_name)):
        template_name = 'info-content.html'
    types = Type.objects.all()
    return render_to_response('short-home.html',
                              {
                                  'authors': Author.objects.all(),
                                  'template_name': template_name,
                                  'types': types,
                                  'location': location,
                                  'locations': Location.objects.all()
                               },
                              context_instance=RequestContext(request))

def home(request):
    l_name = request.session.get('location', None)
    location = Location.objects.get_location(l_name)
    return HttpResponseRedirect(reverse('show_location', args=[location.name]))

def show_location(request, location_name):
    request.session['human'] = True
    location = Location.objects.get_location(location_name)
    if location.name != location_name:
        return HttpResponseRedirect(reverse('show_location', args=[location.name]))
    request.session['location'] = location.name
    return render_to_response('home_new.html',
                              {   'types': Type.objects.all(),
                                  'locations_dropdown': True,
                                  'location': location,
                                  'locations': Location.objects.all()
                                  },
                              context_instance=RequestContext(request))

def show_category(request, location_name, slug):
    location = Location.objects.get_location(location_name)
    if location.name != location_name:
        return HttpResponseRedirect(reverse('show_category', args=[location.name, slug]))
    try:
        category = Type.objects.get(slug=slug)
    except Type.DoesNotExist:
        return HttpResponseRedirect(reverse('show_location', args=[location.name]))
    return render_to_response('home_new.html',
                              {   'types': Type.objects.all(),
                                  'locations_dropdown': True,
                                  'location': location,
                                  'locations': Location.objects.all(),
                                  'category': category
                                  },
                              context_instance=RequestContext(request))
    
def show_object(request, location_name, slug, uid):
    location = Location.objects.get_location(location_name)
    if location.name != location_name:
        return HttpResponseRedirect(reverse('show_category', args=[location.name, slug]))
    try:
        category = Type.objects.get(slug=slug)
    except Type.DoesNotExist:
        return HttpResponseRedirect(reverse('show_location', args=[location.name]))
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    obj = category.get_object(uid, location, acl)
    if obj is None:
        return HttpResponseRedirect(reverse('show_location', args=[location.name]))
    return render_to_response('home_new.html',
                              {   'types': Type.objects.all(),
                                  'locations_dropdown': True,
                                  'location': location,
                                  'locations': Location.objects.all(),
                                  'obj': obj
                                  },
                              context_instance=RequestContext(request))

## def home(request, uid=None, slug=None):
##     request.session['human'] = True;
##     acl = '0'
##     if request.user.is_authenticated():
##         acl = '1'
##         if request.user.is_staff:
##             acl = '2'
##     obj = None
##     uid = uid or request.GET.get('uid')
##     if uid:
##         if re.match('^\d+\-[pt]$', uid):
##             id, t = uid.split('-')
##             if t == 't':
##                 M = Track
##             else:
##                 M = Point
##             qs = M.objects.filter(id=id)
##             if qs.count() != 0:
##                 obj = qs[0]
##         else:
##             qs = Track.objects.filter(uid=uid)
##             if qs.count() != 0:
##                 obj = qs[0]
##             else:
##                 qs = Point.objects.filter(uid=uid)
##                 if qs.count() != 0:
##                     obj = qs[0]
##                 else:
##                     return HttpResponseRedirect('/')
            
##     types = Type.objects.all()
##     #for t in types:
##     #    t.acl = acl

##     if obj is not None and obj.location:
##         if request.session.get('change_location', False):
##             del request.session['change_location']
##             if obj.location.name != request.session.get('location', u'Minsk'):
##                 return HttpResponseRedirect('/')
##         l_name = obj.location.name
##     else:
##         l_name = request.session.get('location', u'Minsk')
##     try:
##         location = Location.objects.get(name=l_name)
##     except Location.DoesNotExist:
##         try:
##             location = Location.objects.filter(default=True)[0]
##         except:
##             location = Location.objects.all()[0]
    
##     return render_to_response('home_new.html',
##                               {   'types': types,
##                                   'obj': obj,
##                                   'locations_dropdown': True,
##                                   'location': location,
##                                   'locations': Location.objects.all()
##                                },
##                               context_instance=RequestContext(request))


def api_doc(request):
    return render_to_response('api-doc.html',
                              {'methods': make_api_doc()},
                              context_instance=RequestContext(request))


from django.utils.translation import activate
def set_language(request):
    next = request.META.get('HTTP_REFERER', '/')
    response = HttpResponseRedirect(next)
    if request.method == 'GET':
        lang_code = request.GET.get('language', None)
        if lang_code:
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    return response

#def set_location(request):
#    next = request.REQUEST.get('next')
#    next = request.META.get('HTTP_REFERER', '/')
#    response = HttpResponseRedirect(next)
#    request.session['location'] = request.GET.get('name', 'Minsk')
#    request.session['change_location'] = True
#    return response

def robots(request):
    return HttpResponse('User-Agent: *\nDisallow: /api/\nDisallow: /language/\nDisallow: /map/',
                        'text/plain')
