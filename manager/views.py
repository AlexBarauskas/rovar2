# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.admin.views.decorators import staff_member_required

from models import Type, Post, Point, Track, EditorImage
from forms import TypeForm, TrackForm, PostForm, PointForm, UploadImageForm
import json

from tmp.parse_xml import XMLTrack


@staff_member_required
def default(request):
    return render_to_response('base_manager.html',
                              {},
                              RequestContext(request))


@staff_member_required
def index(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UploadImageForm()        
    images = EditorImage.objects.all().order_by("-created")[:10]
    return render_to_response('manager_index.html',
                              {'form': form,
                               'images': images},
                              RequestContext(request))

@staff_member_required
def editor_img_del(request, img_id):
    try:
        img = EditorImage.objects.get(id=img_id)
    except ObjectDoesNotExist:
        img = None
        res = {'success': True}
    except:
        res = {'success': False,
               'error': [u'Ошибка при удалении изображения. Повторите попытку.']}
    #
    if img is not None:
        img.delete()
        res = {'success': True}
    #
    return HttpResponse(json.dumps(res),
                        content_type="text/json")


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
    if _type.track_set.count() or _type.point_set.count():
        errors.append(u" Не возможно удалить! Некоторые маршруты или пункты принаджежат данному типу.")
    else:
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
    errors = []
    messages = []
    if track_id is not None:
        track = get_object_or_404(Track, id=track_id)
        title = u'Редактирование маршрута'
    else:
        track=None
        title = u'Новый маршрут'
    if request.method == "POST":
        form = TrackForm(request.POST, request.FILES, instance=track)
        if form.is_valid():

            form.save()
            xml_file = request.FILES.get('xml_coordinates', None)
            created = False
            if track is None:
                track = form.instance
                created = True
            if xml_file:
                try:
                    t = XMLTrack(xml_file.read())                
                    rout = t.get_track()['rout']
                    track.coordinates = json.dumps(rout)
                    track.save()
                except:
                    errors.append(u"Ошибка разбора XML.")
            if not errors:
                messages.append(u"Изменения успешно сохранены.")
            if request.POST.get('submit', 'to_current_page') == 'to_section' and not errors:
                return HttpResponseRedirect(reverse('manager_tracks'))
            if created and not errors:
                return HttpResponseRedirect(reverse('track-edit', 
                                                    args=[form.instance.id]))

    else:
        form = TrackForm(instance=track)
    
    return render_to_response('obj_edit.html',
                              {'form': form,
                               'title': title,
                               'back_url': reverse('manager_tracks'),
                               'info': {'errors': errors,
                                        'messages': messages}
                               },
                              RequestContext(request))
    

@staff_member_required
def track_delete(request, track_id):
    errors = []
    try:
        obj = Track.objects.get(id=track_id)
    except ObjectDoesNotExist:
        errors.append['Object does not exist']
    try:
        obj.delete()
    except e:
        errors.append(str(e))
    res = {
        'success': not errors,
        'errors': errors,
        }
    return HttpResponse(json.dumps(res),
                        content_type="text/json")


@staff_member_required
def post_edit(request, track_id=None, point_id=None):
    if track_id is not None:
        track = get_object_or_404(Track, id=track_id)
        url_name = 'manager_tracks'
    elif point_id is not None:
        track = get_object_or_404(Point, id=point_id)
        url_name = 'manager_points'
    else:
        return HttpResponseNotFound()
    if track.post is None:
        post = Post(title=track.name,
                    text='')
        post.save()
        track.post = post
        track.save()
    else:
        post = track.post
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            if request.POST.get('submit', 'to_current_page') == 'to_section':
                return HttpResponseRedirect(reverse(url_name))

    else:
        form = PostForm(instance=post)
    title = u'Редактирование "%s"' % post.title

    return render_to_response('post_edit.html',
                              {'form': form,
                               'title': title,
                               'back_url': reverse(url_name)
                               },
                              RequestContext(request))
    
def js_image_list(request):
    images = []
    for i in EditorImage.objects.all():
        images.append({'title': i.image.name,
                      'url': i.image.url})
    return render_to_response('tiny_images.js',
                              {'images': images
                               },
                              RequestContext(request),
                              mimetype='text/javascript')
    

@staff_member_required
def points(request):
    points = Point.objects.all()
    return render_to_response('manager_points.html',
                              {'points': points},
                              RequestContext(request))


@staff_member_required
def point_edit(request, point_id=None):
    if point_id is not None:
        point = get_object_or_404(Point, id=point_id)
        title = u'Редактирование точки'
    else:
        point = None
        title = u'Новый маршрут'
    messages = []
    if request.method == "POST":
        form = PointForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            messages.append(u"Изменения успешно сохранены.")
            if request.POST.get('submit', 'to_current_page') == 'to_section':
                return HttpResponseRedirect(reverse('manager_points'))
            if point is None:
                return HttpResponseRedirect(reverse('point-edit', 
                                                    args=[form.instance.id]))
                
    else:
        form = PointForm(instance=point)
    
    return render_to_response('obj_edit.html',
                              {'form': form,
                               'title': title,
                               'back_url': reverse('manager_points'),
                               'info': {'messages': messages},
                               },                              
                              RequestContext(request))

@staff_member_required
def point_delete(request, point_id):
    errors = []
    try:
        obj = Point.objects.get(id=point_id)
    except ObjectDoesNotExist:
        errors.append['Object does not exist']
    try:
        obj.delete()
    except e:
        errors.append(str(e))
    res = {
        'success': not errors,
        'errors': errors,
        }
    return HttpResponse(json.dumps(res),
                        content_type="text/json")

