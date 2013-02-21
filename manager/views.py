from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def default(request):
    return render_to_response('base_manager.html',
                              {},
                              RequestContext(request))


@staff_member_required
def index(request):
    return render_to_response('manager_index.html',
                              {},
                              RequestContext(request))


