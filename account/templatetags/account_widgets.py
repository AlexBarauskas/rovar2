# -*- coding: utf-8 -*-
import os
from django import template
from django.conf import settings
from django.utils import translation

from account.models import Author

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
        u = context.get('request').user
    except AttributeError:
        u = None
    return {'user': u}

