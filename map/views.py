# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse

import json

#from tmp.parse_xml import XMLTrack
from map.models import Track, Point, Type
import json

def get_available_tracks(request):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    query = {'state__lte': acl}
    if 'type' in request.GET:
        try:
            query['type'] = Type.objects.get(id=request.GET['type'])
        except:
            pass
        
    #tracks = Track.objects.filter(state__lte=acl)
    tracks = [t.id for t in Track.objects.filter(**query)]
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
                 'id': t.id,
                 'type': [t.type.obj, '%s' % t.type.id],
                 'color': t.type.color,
                 }
        if t.duration:
            track['duration'] = '%s мин' % t.duration
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
            query['type'] = Type.objects.get(id=request.GET['type'])
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
                 'id': p.id,
                 'color': p.type.color,
                 'marker': '/static/images/Parking.png',
                 'status': 'success',
                 'images': [ph.image.url for ph in  p.photo_set.all()],
                 'address': p.address,
                 }
        if p.type.image:
            point['marker'] = p.type.image.url
        point['type'] = [p.type.obj, '%s' % p.type.id]
        if p.post:
            point['post_url'] = reverse('blog_post', args=[p.post.id])
    except:
        point = {'status': 'error',}
    return HttpResponse(json.dumps(point),
                        mimetype='text/json')
