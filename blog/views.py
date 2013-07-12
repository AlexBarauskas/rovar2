# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.template import RequestContext

from map.models import Point, Track
from blog.models import Post

def blog(request):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    qs = Post.objects.extra(select={'acl_track': 'SELECT state FROM manager_track WHERE post_id=manager_post.id ',
                                    'acl_point': 'SELECT state FROM manager_point WHERE post_id=manager_post.id ',
                                    }).order_by('-created')
    last_posts = []
    for p in qs:
        if (p.acl_track or p.acl_track) and (p.acl_track or p.acl_track) <= acl:
            last_posts.append(p)
            if len(last_posts)>2:
                break
    return render_to_response('blog.html',
                              {'posts': last_posts,
                               'links': Post.objects.get_links(acl)},
                              context_instance=RequestContext(request))

def post(request, post_id):
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    post = get_object_or_404(Post, id=post_id)
    if not Point.objects.filter(post=post, state__lte=acl).count() and not Track.objects.filter(post=post, state__lte=acl).count():
        raise Http404
    return render_to_response('blog.html',
                              {'posts': [post],
                               'currentid': post.id,
                               'links': Post.objects.get_links(acl)},
                              context_instance=RequestContext(request))
