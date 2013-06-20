# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404

from manager.models import Post

def blog(request):
    try:
        last_post = Post.objects.order_by('-created')[0]
    except:
        last_post = None
    return render_to_response('blog.html',
                              {'post': last_post})
    #return HttpResponse('Project run!')

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render_to_response('blog.html',
                              {'post': post})
