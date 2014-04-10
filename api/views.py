# -*- coding: utf-8 -*-
"""@package api
Documentation for this module.

More details.
"""
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import json

from api.models import Application, Message, Track, Point, Type, Photo, Offer
#http://blogs.cs.st-andrews.ac.uk/jfdm/2013/04/04/documenting-python-using-doxygen/


#class API(object):


@csrf_exempt
def initialize_app(request):
    '''@brief Иничиализация клиента.
    POST: http://onbike.by/api/clients
Запрос на инициализацию клиента.\n
Возвращаемый json:
---
    {'success': True,\n'uid': 'peronas_key_for_feedback'}\n
Параметр "uid" клиент должен сохранить на своей стороне и использовать его для получения состояний.
    '''
    if request.method != "POST":
        HttpResponse(json.dumps({'success': False,
                                 'error': "Incorrect method."}), mimetype='text/json')
    try:
        app = Application.objects.create()
        res = {'success': True,
               'uid': app.uid}
    except Exception, e:
        res = {'success': False,
               'errors': '%s' % e}
    return HttpResponse(json.dumps(res), mimetype='text/json')


def points(request):
    '''@brief Получение информации о доступных точках.
    GET: http://onbike.by/api/points?page=P&per_page=N
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
            pass
    if page is not None:
        per_page = request.GET.get('per_page', 10)
        try:
            per_page = int(per_page)
        except:
            per_page = 10
    kwargs = {'state__lte': acl}
    points = Point.objects.filter(**kwargs)
    if page is not None:
        posins = points[page * per_page:(page + 1) * per_page]
    points = [p.to_dict() for p in points]
    return HttpResponse(json.dumps(points),
                        mimetype='text/json')




TYPEIDS = {"entertainment": 7,
           "bikerental": 6,
           "shop": 5,
           "service": 2,
           "parking": 3,
           }
def __string_type_to_object(stype):
    if settings.DEBUG:
        return Type.objects.filter(obj='p')[0]
    try:
        return Type.objects.get(id=TYPEIDS.get(stype))
    except:
        None


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
'''
    # check request type
    if request.method != 'POST':
        return HttpResponse(json.dumps({'success': False,
                                        'error_code': 1,
                                        'message': 'Incorrect method.'
                                        }),
                            mimetype='text/json')
    # check app uid
    uid = request.POST.get('uid', '')
    if Application.objects.filter(uid=uid).count() == 0:
        return HttpResponse(json.dumps({'success': False,
                                        'error_code': 2,
                                        'message': 'Your client is not authorized.'
                                        }),
                            mimetype='text/json')

    # check required fields
    required_fields = ['title', 'type', 'description', 'coordinates', 'address']
    values = [request.POST.get(field) for field in required_fields]
    if all(values):
        kwargs = {'name': values[0],
                  'type': values[1],
                  'description': values[2],
                  'coordinates': values[3],
                  'address': values[4]}
    else:
        return HttpResponse(json.dumps({'success': False,
                                        'error_code': 3,
                                        'message': 'Not all required fields.'
                                        }),
                            mimetype='text/json')
    # check point type
    kwargs['type'] = __string_type_to_object(kwargs['type'])
    if kwargs['type'] is None:
        return HttpResponse(json.dumps({'success': False,
                                        'error_code': 4,
                                        'message': 'Not valid "type".'
                                        }),
                            mimetype='text/json')
    # check image
    photos = request.FILES.getlist('image')
    if len(photos) == 0:
        return HttpResponse(json.dumps({'success': False,
                                        'error_code': 5,
                                        'message': '"image" is required field.'
                                        }),
                            mimetype='text/json')
    # get not required fileds
    kwargs['phones'] = request.POST.get('phones')
    kwargs['website'] = request.POST.get('website')
    # create poin
    p = Point.objects.create(**kwargs)
    # add photos
    for photo in photos:
        Photo.objects.create(point=p,
                             image=photo
                             )
    # create app_message
    app = Application.objects.get(uid=uid)
    app.add_message(point=p)
    return HttpResponse(json.dumps({'success': True}),
                        mimetype='text/json')


def messages(request):
    '''@brief Получение списка сообщений о состояниий заявленных точек.
    GET: http://obike.by/api/messages?uid=<app_uid>
В случае успеха возвращает {'success': True, 'messages': [{'id': <message_id>, 'message': <message_text>}]}
    '''
    messages = Message.objects.filter(app__uid=request.GET.get('uid'), state="f").values('message', 'id')
    return HttpResponse(json.dumps({'success': True,
                                    'messages': list(messages)}),
                        mimetype='text/json')


@csrf_exempt
def message_read(request):
    '''@brief Изменение статуса сообщения на прочитанное.
    POST: http://obike.by/api/messages/read?uid=<app_uid>&id=<message_id>
Параметр "id" есть идентификатор собщения в списке полученных сообщений(см. "http://obike.by/api/messages?uid="<app_uid>).
    '''
    if request.method != "POST":
        HttpResponse(json.dumps({'success': False,
                                 'error': "Incorrect method."}), mimetype='text/json')
    res = {'success': True}
    if not Message.objects.filter(app__uid=request.POST.get('uid'),
                                  id=request.POST.get('id')).update(state='r'):
        res = {'success': False,
               'error': 'Message with id=%s not exists.' % message_id}
    return HttpResponse(json.dumps(res),
                        mimetype='text/json')

    
@csrf_exempt
def point_offer(request):
    '''@brief Предложение по изменению информации о точке.
    POST: http://obike.by/api/points/offer
Параметры:
---
id - ID точки(получен клиентом вместе с информацией о точке)\n
uid - ключ для обратной связи(идентификатор клиента).\n
description - что хотим предложить.
'''
    if request.method != "POST":
        HttpResponse(json.dumps({'success': False,
                                 'error': "Incorrect method."
                                 }),
                     mimetype='text/json')
    # check description
    description = request.POST.get('description', "").strip()
    if not description:
        HttpResponse(json.dumps({'success': False,
                                 'error': "Description is required."
                                 }),
                     mimetype='text/json')
    # check app uid
    uid = request.POST.get('uid', '')
    if Application.objects.filter(uid=uid).count() == 0:
        return HttpResponse(json.dumps({'success': False,
                                        'message': "Your client is not authorized."
                                        }),
                            mimetype='text/json')
    # check point
    pid = request.POST.get('id', '')
    try:
        point = Point.objects.get(id=pid)
    except:
        return HttpResponse(json.dumps({'success': False,
                                        'message': "Object not found."
                                        }),
                            mimetype='text/json')
    
    res = {'success': True}
    app = Application.objects.get(uid=uid)
    offer, c = Offer.objects.get_or_create(point=point,
                                           description=description)
    if c:
        app.add_message(point=point, method="u")
    return HttpResponse(json.dumps(res),
                        mimetype='text/json')
