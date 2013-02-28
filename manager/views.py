from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from django.contrib.admin.views.decorators import staff_member_required

from models import Type
from forms import TypeForm
import json


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


@staff_member_required
def types(request):
    _types = Type.objects.all()
    forms=[]
    if request.method == "POST":
        for t in _types:
            prefix = "%s" % t.id
            f = TypeForm(request.POST, prefix=prefix, instance=t)
            if f.is_valid():
                f.save()
            forms.append(f)
        f = TypeForm(request.POST)
        if f.is_valid():
            f.save()
            forms.append(f)
        forms.append(TypeForm())
    else:
        for t in _types:
            prefix = "%s" % t.id
            forms.append(TypeForm(prefix=prefix, instance=t))
        forms.append(TypeForm())
    
    return render_to_response('manager_types.html',
                              {'forms': forms},
                              RequestContext(request))
    

@staff_member_required
def type_delete(request, type_id):
    errors = []
    try:
        _type = Type.objects.get(id=type_id)
    except ObjectDoesNotExist:
        errors.append['Object does not exist']
    try:
        _type.delete()
    except e:
        errors.append(str(e))
    res = {
        'success': not errors,
        'errors': errors,
        }
    return HttpResponse(json.dumps(res),
                        content_type="text/json")
    
        
