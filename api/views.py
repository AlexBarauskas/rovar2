# -*- coding: utf-8 -*-
"""@package api
Documentation for this module.

More details.
"""
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import translation

from django.core.validators import validate_email
from django.core.validators import URLValidator

import json
from datetime import datetime

from api.models import Application, Message, Track, Point, Type, Photo, Offer
from map.models import Location
#http://blogs.cs.st-andrews.ac.uk/jfdm/2013/04/04/documenting-python-using-doxygen/


#class API(object):

validate_url = URLValidator(verify_exists=False)

def _generate_response(request, data):
    f = request.GET.get('rtype') or request.POST.get('rtype', 'json')
    c = request.GET.get('callback') or request.POST.get('callback', '(function(){})')
    if f == 'js' and c:
        res = '%s(%s);' % (c, json.dumps(data))
        mt = 'text/javascript'
    else:
        res = json.dumps(data)
        mt = 'text/json'
    return HttpResponse(res, mt)

@csrf_exempt
def initialize_app(request):
    '''@brief Иничиализация клиента.
    POST: http://onbike.by/api/clients
Запрос на инициализацию клиента.\n
Возвращаемый json:
---
    {'success': True,\n'uid': 'personal_key_for_feedback'}\n
Параметр "uid" клиент должен сохранить на своей стороне и использовать его для получения состояний.
    '''
    if request.method != "POST":
        return _generate_response(request, {'success': False, 'error': "Incorrect method."})
    try:
        app = Application.objects.create()
        res = {'success': True,
               'uid': app.uid}
    except Exception, e:
        res = {'success': False,
               'errors': '%s' % e}
    return _generate_response(request, res)


def locations(request):
    return _generate_response(request,
                              {'locations': list(Location.objects.all().values_list('name', flat=True)),
                               'success': True})
    

def location(request):
    '''@brief Получение информации о локации.
    '''
    location_name = request.GET.get('name', u'Минск')
    try:
        location = Location.objects.get(name = location_name)
    except Location.DoesNotExist:
        location = Location.objects.filter(default=True)[0]
    res = {'name': location.name,
           'center': [location.center_lat, location.center_lng],
           'bounds': [[location.center_lat - location.radius*0.7071067811865475, location.center_lng - 2*location.radius*0.7071067811865475],
                      [location.center_lat + location.radius*0.7071067811865475, location.center_lng + 2*location.radius*0.7071067811865475]
                      ],
           'id': location.id,
           'radius': location.radius,
           'success': True
           }
    return _generate_response(request, res)


def get_types(request):
    '''@brief Получение информации о всех доступных типах объектов.
    GET: http://onbike.by/api/types
    Возвращаемый json:
    {'object': "point|track", # - Тип объекта 
     'name': "<type_name>",
     'color': "#ffffff",
     'image_a': "<url_to_img>", # - Для точек картинка неактивного состояния, для маршрутов - начало маршрута
     'image_b': "<url_to_img>", # - Для точек картинка активного состояния, для маршрутов - конец маршрута
     'text_id': "type_example", # - Уникальный текстовый идентификатор
    }
    '''
    types = [{u'object': [u'point', u'track'][t.obj == 't'],
              u'name': t.name,
              u'color': t.color,
              u'image_a': t.marker_a(), # - Для точек картинка неактивного состояния, для маршрутов - начало маршрута
              u'image_b': t.marker_b(), # - Для точек картинка активного состояния, для маршрутов - конец маршрута
              u'text_id': t.slug, # - Уникальный текстовый идентификатор
              } for t in  Type.objects.filter(active=True, obj__in=['t', 'p'])]
    return _generate_response(request, types)

def points(request):
    '''@brief Получение информации о доступных точках.
    GET: http://onbike.by/api/points?page=P&per_page=N&location=<id|name>&date=15.03.18-16:09:50&type=<type_text_id>
GET-запрос может не содержать параметров.\n
В случае отсутствия параметра page или не верного преобразования в целочисленное значение, будет возвращен список всех доступных точек.\n
В случае отсутствия или неврно указанного параметра per_page значение по умолчанию принимается 10.\n
Если указан параметр date, будут выгружены точки, которые обновлялись после указанной даты. Это не обязательно новые точки, среди них могут быть точки, у которых обновилось какое-либо поле. Формат даты: '%y.%m.%d-%H:%M:%S'. Неверные даты и неверный формат ингнорируется, считается что параметра нет.\n
Параметр location указывается если нужно выбрать точки определенной локации. Указывается либо наименование локации либо id.\n
Параметр type указывает какого типа точки нужно вытащить 
    '''
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    
    page = None
    per_page = None
    if 'page' in request.GET:
        page = request.GET.get('page', 0)
        try:
            page = int(page)
        except:
            page = None
    if page is not None:
        per_page = request.GET.get('per_page', 10)
        try:
            per_page = int(per_page)
        except:
            per_page = 10
    kwargs = {'state__lte': acl}
    if 'location' in request.GET:
        location = request.GET['location']
        if location.isdigit():
            kwargs['location_id'] = location
        else:
            kwargs['location__name'] = location

    if 'date' in request.GET:
        try:
            print request.GET['date']
            t0 = datetime.strptime(request.GET['date'], '%y.%m.%d-%H:%M:%S')
            print t0
            kwargs['last_update__gte'] = t0
        except:
            pass
    
    points = Point.objects.filter(**kwargs)
    if page is not None:
        points = points[page * per_page:(page + 1) * per_page]
        
    lang_code = translation.get_language()    
    points = [p.to_dict(lang=lang_code) for p in points]
    return _generate_response(request, points)


def __string_type_to_object(stype):
    try:
        return Type.objects.get(slug=stype)
    except:
        return None


@csrf_exempt
def add_point(request):
    '''@brief Добавление точки через приложение.
    POST: http://onbike.by/api/point/add
Параметры:
---
uid - ключ для обратной связи. Если на стороне клиента отсутствует данный идентификатор, то необходимо вызвать метод http://onbike.by/api/init для его получения.\n
title - заголовок для точки (max_length 128)\n
type - тип точки. Допустимые значения: shop, bikerental, entertainment, parking, service\n
description - описание точки (max_legth 256).\n
coordinates - координаты точки. Example: "[53.88988, 27.591129]"\n
address - адрес точки (max_length 256). Example: "ул. Станиславского 11а"\n
phones - телефоны (max_length 128). Могут быть перечислены через запятую. Поле не обязательное. Позже будет указон шаблон для номера\n
website - Не обязательно поле. Мало вероятно что будет использовано при добавлении через клиент.\n
image - фотография точки.\n
Коды ошибок:
---
1 - Неверный тип запроса.\n
2 - Клиент с указанным uid не инициализирован.\n
3 - Одно из полей 'title', 'type', 'description', 'coordinates', 'address' не указано или пустое.\n
4 - Указанный тип точки не существует.\n
5 - Отсутсвует изображение.\n
6 - Введен не валидный URL для поля website.\n
>=100 - Ошибки вебклиента. Для мобильных клиентов возвращаться не должны.\n
'''
    # check request type
    if request.method != 'POST':
        return _generate_response(request,
                                  {'success': False,
                                   'error_code': 1,
                                   'message': 'Incorrect method.'})
    try:
        print request.FILES
        print request.POST
    except Exception, e:
        print "Error POST"
        print e
    uid = request.POST.get('uid', '')
    if Application.objects.filter(uid=uid).count() == 0 or (uid == 'webclient' and not request.session.get('human')):
        return _generate_response(request, {'success': False,
                                        'error_code': 2,
                                        'message': 'Your client is not authorized.'})

    email = request.POST.get('email', '').strip()
    if email != '':
        try:
            validate_email(email)
        except:
            email = ''

    if uid == 'webclient' and email == '':
        return _generate_response(request, {'success': False,
                                        'error_code': 100,
                                        'message': 'Email is required.'})

    # check required fields
    required_fields = ['title', 'type', 'address']
    values = [request.POST.get(field) for field in required_fields]
    values.append(request.POST.get('coordinates[]') or request.POST.get('coordinates'))
    try:
        print values
    except:
        pass
    if all(values):
        kwargs = {'name': values[0],
                  'type': values[1],
                  'description': request.POST.get('description', ''),
                  'address': values[2],
                  'coordinates': values[3]}
    else:
        return _generate_response(request, {'success': False,
                                        'error_code': 3,
                                        'message': 'Not all required fields.'})
    if len(kwargs['description'])>256:
        return _generate_response(request, {'success': False,
                                        'error_code': 7,
                                        'message': 'The "description" should not exceed 256 characters.'
                                        })
    # check point type
    kwargs['type'] = __string_type_to_object(kwargs['type'])
    if kwargs['type'] is None:
        return _generate_response(request, {'success': False,
                                        'error_code': 4,
                                        'message': 'Not valid "type".'
                                        })
    # check image
    photos = request.FILES.getlist('image')
    if len(photos) == 0:
        return _generate_response(request, {'success': False,
                                        'error_code': 5,
                                        'message': '"image" is required field.'
                                        })
    # get not required fileds
    phones = request.POST.getlist('phones')
    if phones is not None:
        phones = ','.join(phones)
    kwargs['phones'] = phones
    kwargs['website'] = request.POST.get('website')
    if kwargs['website']:
        try:
            validate_url(kwargs['website'])
        except:
            return _generate_response(request, {'success': False,
                                            'error_code': 6,
                                            'message': 'Enter a valid website.'
                                            })
    if request.user.is_authenticated and request.user.is_superuser:
        kwargs['state'] = '0'
    # create poin
    p = Point.objects.create(**kwargs)
    
    # add photos
    for photo in photos:
        Photo.objects.create(point=p,
                             image=photo
                             )
    # create app_message
    if not (request.user.is_authenticated and request.user.is_superuser):
        app = Application.objects.get(uid=uid)
        app.add_message(point=p, email=email)
    return _generate_response(request, {'success': True})


def messages(request):
    '''@brief Получение списка сообщений о состояниий заявленных точек.
    GET: http://onbike.by/api/messages?uid=<app_uid>
В случае успеха возвращает {'success': True, 'messages': [{'id': <message_id>, 'message': <message_text>}]}
    '''
    messages = Message.objects.filter(app__uid=request.GET.get('uid'), state="f").values('message', 'id')
    return _generate_response(request, {'success': True,
                               'messages': list(messages)})


@csrf_exempt
def message_read(request):
    '''@brief Изменение статуса сообщения на прочитанное.
    POST: http://onbike.by/api/messages/read
    Параметры:
---
id - ID точки(получен клиентом вместе с информацией о точке)\n
uid - ключ для обратной связи(идентификатор клиента).\n
Параметр "id" есть идентификатор собщения в списке полученных сообщений(см. "http://obike.by/api/messages?uid="<app_uid>).
    '''
    if request.method != "POST":
        return _generate_response(request, {'success': False,
                                 'error': "Incorrect method."})
    res = {'success': True}
    if not Message.objects.filter(app__uid=request.POST.get('uid'),
                                  id=request.POST.get('id')).update(state='r'):
        res = {'success': False,
               'error': 'Message with id=%s not exists.' % request.POST.get('id')}
    return _generate_response(request, res)

    
@csrf_exempt
def point_offer(request):
    '''@brief Предложение по изменению информации о точке.
    POST: http://onbike.by/api/points/offer
Параметры:
---
id - ID точки(получен клиентом вместе с информацией о точке)\n
uid - ключ для обратной связи(идентификатор клиента).\n
description - что хотим предложить.\n
image - фотография точки.
'''
    if request.method != "POST":
        return _generate_response(request, {'success': False,
                                 'error': "Incorrect method."})

    # check description
    description = request.POST.get('description', "").strip()
    if not description:
        return _generate_response(request, {'success': False,
                                 'error': "Description is required."})
    # check app uid
    uid = request.POST.get('uid', '')
    #if Application.objects.filter(uid=uid).count() == 0 :
    if Application.objects.filter(uid=uid).count() == 0 or (uid == 'webclient' and not request.session.get('human')):
        return _generate_response(request, {'success': False,
                                   'message': "Your client is not authorized."})
    # check point
    pid = request.POST.get('id', '')
    try:
        point = Point.objects.get(id=pid)
    except:
        return _generate_response(request, {'success': False,
                                   'message': "Object not found."})
    
    res = {'success': True}
    app = Application.objects.get(uid=uid)
    offer, c = Offer.objects.get_or_create(point=point,
                                           description=description)
    if c:
        msg = app.add_message(point=point, method="u", description=description)
    else:
        msg = Message.object.get(point=point, method="u", description=description)
        
    photos = request.FILES.getlist('image')
    for photo in photos:
        p = Photo.objects.create(offer=offer,
                                 image=photo
                                 )
        msg.photos.add(p)
    return _generate_response(request, res)


def tracks(request):
    '''@brief Получение информации о доступных маршрутах.
    GET: http://onbike.by/api/tracks?page=P&per_page=N
GET-запрос может не содержать параметров.\n
В случае отсутствия параметра page или не верного преобразования в целочисленное значение, будет возвращен список всех доступных точек.\n
В случае отсутствия или неврно указанного параметра per_page значение по умолчанию принимается 10.\n
    '''
    acl = '0'
    if request.user.is_authenticated():
        acl = '1'
        if request.user.is_staff:
            acl = '2'
    page = None
    per_page = None
    if 'page' in request.GET:
        page = request.GET.get('page', 0)
        try:
            page = int(page)
        except:
            page = None
    if page is not None:
        per_page = request.GET.get('per_page', 10)
        try:
            per_page = int(per_page)
        except:
            per_page = 10
    kwargs = {'state__lte': acl}
    if 'location' in request.GET:
        location = request.GET['location']
        if location.isdigit():
            kwargs['location_id'] = location
        else:
            kwargs['location__name'] = location
    tracks = Track.objects.filter(**kwargs)
    if page is not None:
        tracks = tracks[page * per_page:(page + 1) * per_page]
    tracks = [p.to_dict() for p in tracks]
    return _generate_response(request, tracks)
