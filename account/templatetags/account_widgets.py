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
    if not os.path.exists(os.path.join(settings.TEMPLATE_DIRS[0], template_name)):
        template_name = 'info-content.html'
    return {
        'authors': Author.objects.all(),
        'template_name': template_name,
    }
