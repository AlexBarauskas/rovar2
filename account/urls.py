# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    'account.views',
    url(r'^edit/$', "edit", name="account_edit"),
)

