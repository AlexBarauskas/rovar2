# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from django.contrib.admin.views.decorators import staff_member_required

from models import Type, Track
from forms import TypeForm, TrackForm
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
    ## Добавить проверку на наличие связанных компанент
    # в случае присутствия связей выдать ошибку о невозможномти удаления
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
    
        
@staff_member_required
def tracks(request):
    tracks = Track.objects.all()
    return render_to_response('manager_tracks.html',
                              {'tracks': tracks},
                              RequestContext(request))

@staff_member_required
def track_edit(request, track_id=None):
    if track_id is not None:
        track = get_object_or_404(Track, id=track_id)
        title = u'Редактирование маршрута'
    else:
        track=None
        title = u'Новый маршрут'
    if request.method == "POST":
        form = TrackForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            if request.POST.get('submit', 'to_current_page') == 'to_section':
                return HttpResponseRedirect(reverse('manager_tracks'))
    else:
        form = TrackForm(instance=track)
    
    return render_to_response('obj_edit.html',
                              {'form': form,
                               'title': title},
                              RequestContext(request))
    
