# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from account.models import Account, ACCOUNT_BACKENDS

from account.backends.twitter import TwitterBackend

def login_page(request):
    backends = []
    tb = TwitterBackend()
    token, url = tb.get_auth_url(return_to="http://localhost:8000/account/return/twitter")
    for b in ACCOUNT_BACKENDS:
        backends.append({'name': b[0],
                         'title': b[1],
                         'img': '/static/account/img/%s.png' % b[0],
                         'url': url})
    request.session['account_token'] = token
    return render_to_response('account/login.html',
                              {'backends': backends},
                              RequestContext(request))

def login_return(request, backend_name):
    tb = TwitterBackend()
    access_token = tb.get_token(request)
    user_data = tb.get_user_data(access_token)
    return HttpResponse(str(user_data))
