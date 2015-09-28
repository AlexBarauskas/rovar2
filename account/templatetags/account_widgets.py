# -*- coding: utf-8 -*-
import os
from django import template
from django.conf import settings
from django.utils import translation

from account.models import Author
from account.forms import UserCreationForm

register = template.Library()


@register.inclusion_tag('info-widget.html', takes_context=True)
def info_widget(context):
    template_name = 'info/content-%s.html' % translation.get_language()
    template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
    if not os.path.exists(template_path):
        template_name = 'info-content.html'
    return {
        'authors': Author.objects.all(),
        'template_name': template_name,
    }


@register.inclusion_tag('info-user.html', takes_context=True)
def info_user_widget(context):
    try:
        u = context['user']
    except AttributeError:
        u = None
    return {'user': u}


@register.inclusion_tag('info-link.html', takes_context=True)
def info_link_widget(context):
    return {}


@register.inclusion_tag('account/info_user_badges.html', takes_context=True)
def info_user_badges(context):
    try:
        u = context['user']
    except AttributeError:
        u = None

    badges = dict()
    if u:
        badges = {
            "is_full_profile": {'state': u.is_full_profile(), 'popup': "Заполните весь профиль для получения бэйджа!"},
        }
    return {'user': u, 'badges': badges}



@register.inclusion_tag('account/info_user_badges.html', takes_context=True)
def info_user_stats(context):
    try:
        u = context['user']
        likes = u.ratings.all()
        comments = u.comments.all()
    except AttributeError:
        u = None
        likes = []
        comments = []

    return {'user': u, 'likes': len(likes), 'comments': len(comments)}
