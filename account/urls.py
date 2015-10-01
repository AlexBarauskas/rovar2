# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('account.views',
    url(r'^edit/$', "account_edit", name="account_edit"),
    url(r'^profile/edit/$', "profile_edit", name="profile_edit"),
    url(r'^profile/(?P<username>[^/]+)/$', "profile", name="account_profile"),
)
