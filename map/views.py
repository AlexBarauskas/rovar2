# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse

import json

#from tmp.parse_xml import XMLTrack
from manager.models import Track, Point, Type
import json

def get_available_tracks(request):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    tracks = Track.objects.filter(state__lte=acl)
    tracks = [t.id for t in tracks]
    
    return HttpResponse(json.dumps({'ids': tracks}),
                        mimetype='text/json')

def track(request, track_id=None):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    kwargs = {'state__lte': acl}
    if track_id:
        kwargs['id'] = track_id
    try:
        t = Track.objects.get(**kwargs)
        track = {'route': json.loads(t.coordinates),
                 'title': t.name,
                 'description': t.description,
                 'video': t.video or '',
                 'id': t.id}
        if t.post:
            track['post_url'] = reverse('blog_post', args=[t.post.id])

    except:
        track = {'route': [[0,0],[0,0]]}

    return HttpResponse(json.dumps(track),
                        mimetype='text/json')

def get_available_points(request):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    query = {'state__lte': acl}
    if 'type' in request.GET:
        try:
            query['type'] = Type.objects.get(name=request.GET['type'])
        except:
            pass
    points = [p.id for p in Point.objects.filter(**query)]
    return HttpResponse(json.dumps({'ids': points}),
                        mimetype='text/json')


def point(request, point_id=None):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    kwargs = {'state__lte': acl}
    if point_id:
        kwargs['id'] = point_id
    try:
        p = Point.objects.get(**kwargs)
        point = {'coordinates': json.loads(p.coordinates),
                 'title': p.name,
                 'description': p.description,
                 'id': p.id}
        if p.type.name == u'Велопарковки':
            point['type'] = 'p'
        elif p.type.name == u'Сервисы':
            point['type'] = 's'
        if p.post:
            point['post_url'] = reverse('blog_post', args=[p.post.id])
    except:
        point = {'coordinates': [0,0]}
    return HttpResponse(json.dumps(point),
                        mimetype='text/json')
