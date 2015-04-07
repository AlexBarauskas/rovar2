# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from map.models import Type, Point, Track, Photo, Translation, Location
from manager.models import EditorImage
from blog.models import Post
from forms import TypeForm, TrackForm, PostForm, PointForm, UploadImageForm, MessageForm, BasePointForm, TransForm, TransFormTrack
import json
import os
import re
from django.views.decorators.csrf import csrf_exempt
from django.utils import translation

from tmp.parse_xml import XMLTrack

from api.models import Message


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
    
    if img is not None:
        img.delete()
        res = {'success': True}
    
    return HttpResponse(json.dumps(res),
                        content_type="text/json")


@staff_member_required
def types(request):
    _types = Type.objects.all()
    forms=[]
    if request.method == "POST":
        for t in _types:
            prefix = "%s" % t.id
            f = TypeForm(request.POST, request.FILES, prefix=prefix, instance=t)
            if f.is_valid():
                f.save()
            forms.append(f)
        f = TypeForm(request.POST, request.FILES)
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
@csrf_exempt
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


@csrf_exempt
def xml_to_coordinates(request):
    data = None
    if 'track-from-xml' in request.FILES:
        t = XMLTrack(request.FILES['track-from-xml'].read())
        data = t.get_track()['rout']
    return HttpResponse(json.dumps(data),
                        content_type="text/json")


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
    trans_forms = []
    
    if request.method == "POST":
        form = TrackForm(request.POST, request.FILES, instance=track)
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code != settings.LANGUAGE_CODE:
                if track is not None:
                    trans, c = Translation.objects.get_or_create(track=track, language=lang_code)
                else:
                    trans = None
                trans_forms.append(TransFormTrack(request.POST, instance=trans, prefix=lang_code))
        if form.is_valid() and all([i.is_valid() for i in trans_forms]):
            _track = form.save()
            for i in trans_forms:
                t = i.save()
                if not t.language:
                    t.language = i.prefix
                if t.track is None:
                    t.track = _track
                t.save()

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
                    track.full_coordinates = json.dumps(rout)
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
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code != settings.LANGUAGE_CODE:
                if track is not None:
                    trans, c = Translation.objects.get_or_create(track=track, language=lang_code)
                else:
                    trans = None
                trans_forms.append(TransFormTrack(instance=trans, prefix=lang_code))
    
    return render_to_response('obj_edit.html',
                              {'form': form,
                               'comments_instance': track,
                               'title': title,
                               'trans_forms': trans_forms,
                               'back_url': reverse('manager_tracks'),
                               'info': {'errors': errors,
                                        'messages': messages}
                               },
                              RequestContext(request))
    

@staff_member_required
@csrf_exempt
def track_delete(request, track_id):
    errors = []
    try:
        obj = Track.objects.get(id=track_id)
    except ObjectDoesNotExist:
        errors.append('Object does not exist')
    try:
        obj.delete()
    except Exception, e:
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
    q = {}
    if 'current_pointfilter' in request.session:
        q = request.session['current_pointfilter']
    if 'type' in request.GET:
        q['type__slug'] = request.GET['type']
        if q['type__slug'] == 'all':
            del q['type__slug']
    if 'location' in request.GET:
        q['location__name'] = request.GET['location']
        if q['location__name'] == 'all':
            del q['location__name']
    if 'location__name' in q and Location.objects.filter(admins=request.user, name=q['location__name']):
        if 'location__id__in' in q:
            del q['location__id__in']
    else:
        if 'location__name' in q:
            del q['location__name']
        q['location__id__in'] = [i[0] for i in Location.objects.filter(admins=request.user).values_list('id')]
            
    points = Point.objects.filter(**q).order_by('-created')
    request.session['current_pointfilter'] = q
    types = Type.objects.filter(obj='p')
    return render_to_response('manager_points.html',
                              {'points': points,
                               'types': types,
                               'cur_type': q.get('type__slug', 'all'),
                               'cur_location': q.get('location__name', 'all'),
                               'locations': Location.objects.filter(admins=request.user),
                               },
                              RequestContext(request))


@staff_member_required
def point_edit(request, point_id=None):
    #start_acl = None
    if point_id is not None:
        point = get_object_or_404(Point, id=point_id)
        title = u'Редактирование точки'
        #start_acl = point.state
    else:
        point = None
        title = u'Новая точка'
    if point is not None and not point.location.admins.filter(id=request.user.id).count():
        return HttpResponseNotFound()

    messages = []
    trans_forms = []
    if request.method == "POST":
        form = PointForm(request.POST, request.FILES,  instance=point)
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code != settings.LANGUAGE_CODE:
                if point is not None:
                    trans, c = Translation.objects.get_or_create(point=point, language=lang_code)
                else:
                    trans = None
                trans_forms.append(TransForm(request.POST, instance=trans, prefix=lang_code))
        if form.is_valid() and all([i.is_valid() for i in trans_forms]):
            _point =  form.save()
            for i in trans_forms:
                t = i.save()
                if not t.language:
                    t.language = i.prefix
                if t.point is None:
                    t.point = _point
                t.save()
            for f in request.FILES.getlist('photos',[]):
                ph = Photo.objects.get_or_create(point=_point, image=f)
            messages.append(u"Изменения успешно сохранены.")
            if request.POST.get('submit', 'to_current_page') == 'to_section':
                return HttpResponseRedirect(reverse('manager_points'))
            if point is None:
                return HttpResponseRedirect(reverse('point-edit', 
                                                    args=[form.instance.id]))
    else:
        form = PointForm(instance=point)
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code != settings.LANGUAGE_CODE:
                if point is not None:
                    trans, c = Translation.objects.get_or_create(point=point, language=lang_code)
                else:
                    trans = None
                trans_forms.append(TransForm(instance=trans, prefix=lang_code))
    mod_notifi = None
    if point is not None and point.message_set.filter(state='m').count():
        mod_notifi = point.message_set.filter(state='m')[0]
    
    return render_to_response('obj_edit.html',
                              {'form': form,
                               'trans_forms': trans_forms,
                               'comments_instance': point,
                               'title': title,
                               'back_url': reverse('manager_points'),
                               'info': {'messages': messages},
                               #'mod_notifi': mod_notifi
                               },                              
                              RequestContext(request))

@staff_member_required
@csrf_exempt
def point_delete(request, point_id):
    errors = []
    try:
        obj = Point.objects.get(id=point_id)
    except ObjectDoesNotExist:
        errors.append('Object does not exist')
    if not obj.location.admins.filter(id=request.user.id).count():
        HttpResponse(json.dumps({'success': False,
                                 'errors': [u'Access denied!'],
                                 }
                                ),
                     content_type="text/json")
    try:
        obj.delete()
    except Exception, e:
        errors.append(str(e))
    res = {
        'success': not errors,
        'errors': errors,
        }
    return HttpResponse(json.dumps(res),
                        content_type="text/json")

@staff_member_required
@csrf_exempt
def photo_img_del(request, point_id, img_id):
    try:
        img = Photo.objects.get(id=img_id)
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


from account.models import Author
from django.template.loaders import app_directories

@staff_member_required
def info_page_edit(request):
    default_template = app_directories.Loader().load_template('info-content.html')[0].origin.name
    template_name = 'info/content-%s.html' % request.GET.get('language', settings.LANGUAGE_CODE)
    template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
    if not os.path.exists(template_path):
        tf = open(template_path, 'w')
        tf.write(open(template_path).read())
        tf.close()
    messages = []
    if request.method == "POST":
        content = request.POST.get('content', u'').strip().encode('utf-8')
        author_filed = re.compile(r'(\d+)_(\w+)')
        if content:
            tf = open(template_path, 'w')
            tf.write(content)
            tf.close()
        authors = {}
        for key, value in request.POST.iteritems():
            field = author_filed.findall(key)
            if field and value:
                field = field[0]
                if field[0] not in authors:
                    authors[field[0]] = {}
                authors[field[0]][field[1]] = value.strip()
        for q, v in authors.iteritems():
            Author.objects.filter(id=q).update(**v)
        for key, value in request.FILES.iteritems():
            field = author_filed.findall(key)
            if field:
                aid = field[0][0]
                try:
                    a = Author.objects.get(id=aid)
                    a.image = value
                    a.save()
                except:
                    pass

        messages.append({'class': 'success',
                         'text': u'Изменения успешно сохранены.'})
    return render_to_response('info_edit.html',
                              {'show_left_panel': True,
                               'messages': messages,
                               'authors': Author.objects.all(),
                               'template_name': template_name,
                               'LC': request.GET.get('language', settings.LANGUAGE_CODE)
                               },                              
                              RequestContext(request))



@staff_member_required
def moderation_objects(request):
    if 'current_modfilter' in request.session:
        q = request.session['current_modfilter']
    else:
        q = {'state': 'm'}
    if 'state' in request.GET:
        q['state'] = request.GET['state']
        if q['state'] == 'all':
            del q['state']
    if 'type' in request.GET:
        q['point__type__slug'] = request.GET['type']
        if q['point__type__slug'] == 'all':
            del q['point__type__slug']
    if 'location' in request.GET:
        q['point__location__name'] = request.GET['location']
        if q['point__location__name'] == 'all':
            del q['point__location__name']
            
    if 'point__location__name' in q and Location.objects.filter(admins=request.user, name=q['point__location__name']):
        if 'point__location__id__in' in q:
            del q['point__location__id__in']
    else:
        if 'point__location__name' in q:
            del q['point__location__name']        
        q['point__location__id__in'] = [i[0] for i in Location.objects.filter(admins=request.user).values_list('id')]
    request.session['current_modfilter'] = q
    messages = Message.objects.filter(**q).order_by('-created')
    return render_to_response('manager_moderation.html',
                              {'objects': messages,
                               'types': Type.objects.filter(obj='p'),
                               'cur_type': q.get('point__type__slug', 'all'),
                               'cur_state': q.get('state', 'm'),
                               'cur_location': q.get('point__location__name', 'all'),
                               'locations': Location.objects.filter(admins=request.user),
                               },                              
                              RequestContext(request))
    
@staff_member_required
def moderation_object(request, message_id):
    messages = []
    message = get_object_or_404(Message, id=message_id, point__isnull=False)
    if not message.point.location.admins.filter(id=request.user.id).count():
        return HttpResponseNotFound()
    form = None
    if request.method == "POST":
        if message.app.uid != 'webclient':
            mform = MessageForm(request.POST, instance=message)
        else:
            mform = None
        if message.point:
            form = BasePointForm(request.POST, instance=message.point, prefix="point")
    else:
        if message.app.uid != 'webclient':
            mform = MessageForm(instance=message)
        else:
            mform = None
        if message.point:
            form = BasePointForm(instance=message.point, prefix="point")
    if request.method == "POST":
        if all([mform is None or mform.is_valid(), form.is_valid()]):
            if mform is not None:
                mform.save()
            form.save()
            messages.append(u'Изменения успешно сохранены')
    return render_to_response('manager_moderation_obj.html',
                              {'obj': message,
                               'info': {'messages': messages},
                               'mform': mform,
                               'form': form
                               },                              
                              RequestContext(request))

@staff_member_required
def get_translate_point(request):
    return HttpResponse(Point.objects.to_translate_manager(), mimetype="text/plain")


@staff_member_required
@csrf_exempt
def moderation_object_delete(request, message_id):
    errors = []
    try:
        obj = Message.objects.get(id=message_id)
    except ObjectDoesNotExist:
        errors.append('Object does not exist')
    if not obj.point.location.admins.filter(id=request.user.id).count():
        errors.append('Object does not exist')
    else:
        try:
            if obj.method == 'a':
                obj.point.delete()
                obj.delete()
        except Exception, e:
            errors.append(str(e))
        res = {
            'success': not errors,
            'errors': errors,
            }
    return HttpResponse(json.dumps(res),
                        content_type="text/json")
