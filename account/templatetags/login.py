# from django import template
# from django.core.urlresolvers import reverse
# from django.utils.translation import ugettext_lazy as _
# from account.models import Account, ACCOUNT_BACKENDS

# register = template.Library()

# @register.inclusion_tag('account/login_popup.html', takes_context=True)
# def login_form(context):
#     backends = []
#     for b in ACCOUNT_BACKENDS:
#         backends.append({'name': b[0],
#                          'title': b[1],
#                          'img': '/static/account/img/%s.png' % b[0],
#                          'url': reverse('login_start', args=[b[0]])})
#     context.update({'backends': backends})
#     return context
