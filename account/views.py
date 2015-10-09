# -*- coding: utf-8 -*-
import json
from django.core import serializers
from account.models import User, Rating
from account.forms import UserAccountForm, UserProfileForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login, authenticate
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.apps.django_app.utils import psa
from blog.models import Comment


def context(**extra):
    return dict({
        'plus_id': getattr(settings, 'SOCIAL_AUTH_GOOGLE_PLUS_KEY', None),
        'plus_scope': ' '.join(GooglePlusAuth.DEFAULT_SCOPE),
        'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)
    }, **extra)


@render_to('map.html')
def require_email(request):
    backend = request.session['partial_pipeline']['backend']
    return context(email_required=True, backend=backend)


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


@psa('social:complete')
def ajax_auth(request, backend):
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')


@login_required(login_url='/')
def account_edit(request):
    if request.method == 'GET':
        form = UserAccountForm(instance=request.user)
    else:
        form = UserAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password='')
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect(reverse('account_edit'))
    return render(request, 'account/edit/account.html', {'form': form,})

@login_required(login_url='/')
def profile_edit(request):
    if request.method == 'GET':
        form = UserProfileForm(instance=request.user)
    else:
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password='')
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect(reverse('profile_edit'))
    return render(request, 'account/edit/profile.html', {'form': form,})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'account/profile.html', {'user': user,})

@login_required(login_url='/')
def comments_edit(request):
    comments = Comment.objects.filter(owner=request.user)
    return render(request, 'account/edit/comments.html', {'comments': comments,})

@login_required(login_url='/')
def rating_edit(request):
    ratings = Rating.objects.filter(owner=request.user)
    return render(request, 'account/edit/rating.html', {'ratings': ratings,})

