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
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'

    ## try:
    ##     parking_type = Type.objects.get(obj='p', name=u"Велопарковки")
    ##     parkings = parking_type.point_set.filter(state__lte=acl).count()
    ## except:
    ##     parkings = 0

    ## try:
    ##     services_type = Type.objects.get(obj='p', name=u"Сервисы")
    ##     services = services_type.point_set.filter(state__lte=acl).count()
    ## except:
    ##     services = 0

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
    return render_to_response('home.html',
                              {'tracks': Track.objects.filter(state__lte=acl),
                               #'services': services,
                               #'parkings': parkings,
                               'types': types,
                               'rovar_uid': uid,
                               'obj': obj,
                               },
                              context_instance=RequestContext(request))

#@login_required
def info(request):
    return render_to_response('info.html',
                              {'authors': Author.objects.all(),
                               'show_left_panel': not request.GET.get('blank')},
                              context_instance=RequestContext(request))
    
