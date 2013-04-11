# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

from account.models import Account, ACCOUNT_BACKENDS
from account.backends import DenyException
from account.backends.twitter import TwitterBackend

def login_page(request):
    #print request.user.is_authenticated()
    backends = []
    for b in ACCOUNT_BACKENDS:
        backends.append({'name': b[0],
                         'title': b[1],
                         'img': '/static/account/img/%s.png' % b[0],
                         'url': reverse('login_start', args=[b[0]])})
    return render_to_response('account/login.html',
                              {'backends': backends},
                              RequestContext(request))

def login_start(request, backend_name):
    backend = TwitterBackend()
    redirect_url = request.META.get('HTTP_REFERER','/')
    print redirect_url
    request.session['post_login_redirect'] = redirect_url
    return_url = "http://%s%s" % (settings.MAIN_HOST,
                                  reverse('login_return', args=[backend_name]))
    token, url = backend.get_auth_url(return_to=return_url)
    request.session['account_token'] = token
    return HttpResponseRedirect(url)

def login_return(request, backend_name):
    backend = TwitterBackend()
    redirect_url = request.session.get('post_login_redirect', '/')
    try:
        access_token = backend.get_token(request)
    except DenyException:
        return HttpResponseRedirect(redirect_url)
    except:
        return HttpResponse(u'Ошибка авторизации!')

    user_data = backend.get_user_data(access_token)
    
    #if not request.user.is_authenticated():
    account = Account.objects.filter(id_from_backend=user_data['id'],
                                     backend=backend_name,
                                     )
    if account.count():
        account = account[0]
        user = account.user
        user = authenticate(username=user.username, password=2)
        login(request, user)
        return HttpResponseRedirect(redirect_url)
    if not request.user.is_authenticated():
        un = "%s - %s" % (user_data['screen_name'], user_data['id'])
        user, created = User.objects.get_or_create(username=un)
        if created:
            temp_password = User.objects.make_random_password(length=12)
            user.set_password(temp_password)
        user.first_name = user_data['name']
        user.save()
        user = authenticate(username=user.username, password=2)
    else:
        user = request.user
    account = Account(user=user,
                      name=user.first_name,
                      img_url=user_data['picture'],
                      backend=backend_name,
                      id_from_backend=user_data['id'],
                      ) 
    account.save()
    login(request, user)
    return HttpResponseRedirect(redirect_url)
