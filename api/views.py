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
from blog.models import Post, Comment
#http://blogs.cs.st-andrews.ac.uk/jfdm/2013/04/04/documenting-python-using-doxygen/


#class API(object):

validate_url = URLValidator()#verify_exists=False)

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
    '''-Инициализация клиента.
    POST: http://onbike.by/api/clients
    Запрос на инициализацию клиента.
    --Возвращаемый json:
    {'success': true,
    'uid': 'personal_key_for_feedback'
    }
    Параметр "uid" клиент должен сохранить на своей стороне и использовать его для получения состояний.
    '''
    #if request.method != "POST": # iOS отстает временно игнорируем проверку метода запроса
    #    return _generate_response(request, {'success': False, 'error': "Incorrect method."})
    try:
        app = Application.objects.create()
        res = {'success': True,
               'uid': app.uid}
    except Exception, e:
        res = {'success': False,
               'errors': '%s' % e}
    return _generate_response(request, res)


def locations(request):
    '''-Получение списка доступных локаций.
    GET: http://onbike.by/api/locations
    Получение списка доступных локаций.
    --Возвращаемый json:
    {'locations': ["locale_name_1", "locale_name_2", ...],
    'success': true
    }
    '''
    return _generate_response(request,
                              {'locations': list(Location.objects.all().values_list('name', flat=True)),
                               'success': True})
    

def location(request):
    '''-Получение информации о локации.
    GET: http://onbike.by/api/location?name=<LocationName>;
    Получение информации о локации.
    --Возвращаемый json:
    {'name': "Test",
    'center': [53.9, 27.566667], <b>//- координаты центра</b>
    'bounds': [[53.73909273331522, 27.24485246663044], [54.06090726668478, 27.888481533369557]], <b>//- прямоугольная область, ограничивающая локацию</b>
    'radius': 0.22, <b>//- на основании этого параметра строится bounds. Можно использовать если накладываются специфичные ограничения на отображение нарты.</b>
    'id': 1,
    'success': true
    }
    В случае если по заданному name не была найдена локация, будет возвращена локация по умолчанию(на данный момент Минск).
    '''
    location_name = request.GET.get('name', u'Minsk')
    try:
        location = Location.objects.get(name = location_name)
    except Location.DoesNotExist:
        location = Location.objects.filter(default=True)[0]
    res = {'name': location.name,
           'display_name': location.display_name,
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
    '''-Получение информации о всех доступных типах объектов.
    GET: http://onbike.by/api/types
    
    --Возвращаемый json:
    {'object': "point|track", // - <b>Тип объекта</b>
     'name': "type_name",
     'color': "#ffffff",
     'marker_a': "<url_to_img>", // - <b>Для точек картинка неактивного состояния, для маршрутов - начало маршрута</b>
     'marker_b': "<url_to_img>", // - <b>Для точек картинка активного состояния, для маршрутов - конец маршрута</b>
     'text_id': "type_example", // - <b>Уникальный текстовый идентификатор</b>
    }
    '''
    types = [{u'object': [u'point', u'track'][t.obj == 't'],
              u'name': t.name,
              u'color': t.color,
              u'marker_a': t.marker_a(), # - Для точек картинка неактивного состояния, для маршрутов - начало маршрута
              u'marker_b': t.marker_b(), # - Для точек картинка активного состояния, для маршрутов - конец маршрута
              u'text_id': t.slug, # - Уникальный текстовый идентификатор
              } for t in Type.objects.filter(active=True, obj__in=['t', 'p'])]
    return _generate_response(request, types)

def points(request):
    '''-Получение информации о доступных точках.
    GET: http://onbike.by/api/points?page=P&per_page=N&location=<id|name>&date=<time>&type=<type_text_id>&id=point_id
Запрос может не содержать параметров.
В случае отсутствия параметра page или не верного преобразования в целочисленное значение, будет возвращен список всех доступных точек.
В случае отсутствия или неврно указанного параметра per_page значение по умолчанию принимается 10.
Если указан параметр date, будут выгружены точки, которые обновлялись после указанной даты. Это не обязательно новые точки, среди них могут быть точки, у которых обновилось какое-либо поле. Формат даты: <b>'%y.%m.%d-%H:%M:%S'</b>. Неверные даты и неверный формат ингнорируется, считается что параметра нет.
Параметр location указывается если нужно выбрать точки определенной локации. Указывается либо наименование локации либо id.
Параметр type указывает какого типа точки нужно вытащить.

    --Возвращаемый json:
    [{
    'coordinates': [lat, lon], <b>// - Или наоборот</b>
    'title': "ГУМ",
    'description': "Велопарковка около ГУМа",
    'id': 33,
    'status': 'success',
    'images': ["/link/to/img1", "/link/to/img2", ... ],
    'address': "пр.Независимости 21",
    'uid': "GUM", <b>// - Идентификатор для ссылки</b>
    'type_slug': "parking", <b>// - Уникальный текстовый идентификатор типа к которому принадлежит точка.</b>
    'website': null,
    'comments_count': количество комментариев,
    'color': "#cffcdf", <b>// - Цвет Маркера. В скором будущем будет удалено.</b>
    'marker': "/url/to/marker", <b>// - Маркер неактивного состояния. В скором будущем будет удалено.</b>
    'marker_active': "/url/to/marker_active", <b>// - Марке активного состояния. В скором будущем будет удалено.</b>
    'type_name': "Парковка", <b>// - Наименование типа. В скором будущем будет удалено.</b>
    }, ... ]
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
        
    if 'id' in request.GET:
        kwargs['id__in'] = request.GET.getlist('id')
        
    if 'type' in request.GET:
        kwargs['type__slug'] = request.GET['type']

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
    '''-Добавление точки через приложение.
    POST: http://onbike.by/api/point/add
--Параметры:
uid - ключ для обратной связи. Если на стороне клиента отсутствует данный идентификатор, то необходимо вызвать метод http://onbike.by/api/init для его получения.
title - заголовок для точки (max_length 128)
type - тип точки. Допустимые значения: shop, bikerental, entertainment, parking, service
description - описание точки (max_legth 256).
coordinates - координаты точки. Example: "[53.88988, 27.591129]"
address - адрес точки (max_length 256). Example: "ул. Станиславского 11а"
phones - телефоны (max_length 128). Могут быть перечислены через запятую. Поле не обязательное. Позже будет указон шаблон для номера
website - Не обязательно поле. Мало вероятно что будет использовано при добавлении через клиент.
image - фотография точки.
--Коды ошибок:
1 - Неверный тип запроса.
2 - Клиент с указанным uid не инициализирован.
3 - Одно из полей 'title', 'type', 'description', 'coordinates', 'address' не указано или пустое.
4 - Указанный тип точки не существует.
5 - Отсутсвует изображение.
6 - Введен не валидный URL для поля website. URL не является обязательным параметром, но должен быть введен корректно.
>=100 - Ошибки вебклиента. Для мобильных клиентов возвращаться не должны.

--Возвращаемый json:
{'success': false,
'error_code': 1,
'message': "Error message."
}
В случае успеха:
{'success': true}
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
    '''-Получение списка сообщений о состояниий заявленных точек.
    GET: http://onbike.by/api/messages?uid=<app_uid>
    --Возвращаемый json:
    {'success': true,
    'messages': [{'id': <message_id>, 'message': <message_text>}]
    }
    '''
    messages = Message.objects.filter(app__uid=request.GET.get('uid'), state="f").values('message', 'id')
    return _generate_response(request, {'success': True,
                               'messages': list(messages)})


@csrf_exempt
def message_read(request):
    '''-Изменение статуса сообщения на прочитанное.
    POST: http://onbike.by/api/messages/read
    --Параметры:
    id - ID точки(получен клиентом вместе с информацией о точке)
    uid - ключ для обратной связи(идентификатор клиента).
    Параметр "id" есть идентификатор собщения в списке полученных сообщений(см. "http://obike.by/api/messages?uid="<app_uid>).
    --Коды ошибок:
    1 - Неверный тип запроса.
    2 - Сообщение с указанным id не найдено.

    --Возвращаемый json:
    {'success': false,
    'error_code': 1,
    'message': "Incorrect method."
    }
    В случае успеха:
    {'success': true}
    '''
    
    if request.method != "POST":
        return _generate_response(request, {'success': False,
                                            'error_code': 1,
                                            'message': "Incorrect method."
                                            })
    res = {'success': True}
    if not Message.objects.filter(app__uid=request.POST.get('uid'),
                                  id=request.POST.get('id')).update(state='r'):
        res = {'success': False,
               'error_code': 2,
               'message': 'Message with id=%s not exists.' % request.POST.get('id')}
    return _generate_response(request, res)

    
@csrf_exempt
def point_offer(request):
    '''-Предложение по изменению информации о точке.
    POST: http://onbike.by/api/points/offer
    --Параметры:
    id - ID точки(получен клиентом вместе с информацией о точке)
    uid - ключ для обратной связи(идентификатор клиента).
    description - что хотим предложить.
    image - фотография точки.

    --Коды ошибок:
    1 - Неверный тип запроса.
    2 - Клиент с указанным uid не инициализирован.
    3 - Полу 'description' является обязательным.
    4 - Указанная точка не найдена.

    --Возвращаемый json:
    {'success': false,
    'error_code': 1,
    'message': "Incorrect method."
    }
    В случае успеха:
    {'success': true}
    '''
    if request.method != "POST":
        return _generate_response(request, {'success': False,
                                            'error_code': 1,
                                            'message': "Incorrect method."
                                            })

    # check description
    description = request.POST.get('description', "").strip()
    if not description:
        return _generate_response(request, {'success': False,
                                            'error_code': 3,
                                            'message': "Description is required."})
    # check app uid
    uid = request.POST.get('uid', '')
    #if Application.objects.filter(uid=uid).count() == 0 :
    if Application.objects.filter(uid=uid).count() == 0 or (uid == 'webclient' and not request.session.get('human')):
        return _generate_response(request, {'success': False,
                                            'error_code': 2,
                                            'message': "Your client is not authorized."})
    # check point
    pid = request.POST.get('id', '')
    try:
        point = Point.objects.get(id=pid)
    except:
        return _generate_response(request, {'success': False,
                                            'error_code': 4,
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
    '''-Получение информации о доступных маршрутах.
    GET: http://onbike.by/api/tracks?page=P&per_page=N&location=<id|name>&type=<type_text_id>&id=track_id
    Запрос может не содержать параметров.\n
    В случае отсутствия параметра page или не верного преобразования в целочисленное значение, будет возвращен список всех доступных точек.\n
    В случае отсутствия или неврно указанного параметра per_page значение по умолчанию принимается 10.\n
    --Возвращаемый json:
    [{
    "description": "Маршрут от ст.м. Каменная Горка до проспекта Независимости (в районе пересечения с ул.Городской Вал)",
    "color": "#e67e22", <b>// - Цвет линии</b>
    "type_slug": "track", <b>// - Идентификатор типа</b>
    "video": "&lt;iframe width="560" height="315" src="http://www.youtube.com/embed/olq6cljXcRU" frameborder="0" allowfullscreen&gt;&lt;/iframe&gt;;", <b>// - Код для вставки видео</b>
    "duration": "29 мин", <b>// - Длительность маршрута</b>
    "id": 13, <br/>
    "uid": "13-t", <b>// - Идентификатор для ссылки</b>
    "marker_b": "/media/icons/pin-route-b.png", <b>// - Маркер начала</b>
    "marker_a": "/media/icons/pin-route-a.png", <b>// - Маркер окончания</b>
    "title": "Кунцевщина - Центр", <b>// - Наименование</b>
    "route": [[1,2], ... ], <b>// - Список координат</b>
    "type_name": "Маршруты", <b>// - Наимениванеи типа маршрута</b>
    "type": ["t", "1"], <b>// - Код типа.</b>
    }, ... ]
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
    if 'id' in request.GET:
        kwargs['id__in'] = request.GET.getlist('id')
        
    if 'type' in request.GET:
        kwargs['type__slug'] = request.GET['type']

    tracks = Track.objects.filter(**kwargs)
    if page is not None:
        tracks = tracks[page * per_page:(page + 1) * per_page]
    tracks = [p.to_dict() for p in tracks]
    return _generate_response(request, tracks)


def __get_post(src_entry):
    """
        Функция возвращает инстанс Post соотвествующей модели Point или Track
        Если его нет, то надо бы создать
    """
    if not src_entry.post:
        entry = Post.objects.create(title=src_entry.name, text=src_entry.description)
        src_entry.post = entry
        src_entry.save()
    return src_entry.post


def __get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def __html_special_chars(text):
    return text \
            .replace(u"&", u"&amp;") \
            .replace(u'"', u"&quot;") \
            .replace(u"'", u"&#039;") \
            .replace(u"<", u"&lt;") \
            .replace(u">", u"&gt;")


def comments(request):
    """
    [point:point_id, :limit, :skip]/
    -Получение информации о доступных маршрутах.
    GET: http://onbike.by/api/comments?entry_type=<type>&entry_id=<id>&page=P&per_page=N

    entry_type=<type> - тип сущности (Point|Track|Post)
    entry_id=<id> - ID - сущности к которой отдать комментарии

        comments = [
        {
          "id": 1,
          "username": "Admin",
          "is_auth": True,
          "timestamp": "date1",
          "message": "Тут большой комментарий1",
          "parent_id": None,
          },
        ]

        Если комментариев нет то приходит:
        {
            empty : true
        }
    """

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

    if 'entry_id' in request.GET:
        entry_id = request.GET.get('entry_id')
        try:
            entry_id = int(entry_id)
        except:
            raise ValueError
    else:
        raise ValueError

    if 'entry_type' in request.GET:
        entry_type = request.GET.get('entry_type')
        if entry_type == 'Point':
            src_entry = Point.objects.get(pk=entry_id)
            entry = __get_post(src_entry)
        elif entry_type == 'Track':
            src_entry = Track.objects.get(pk=entry_id)
            entry = __get_post(src_entry)
        elif entry_type == 'Post':
            entry = Post.objects.get(pk=entry_id)
    else:
        raise ValueError

    comments = Comment.objects.filter(post=entry)
    if not comments:
        return _generate_response(request, {"empty": True})

    # from time import sleep
    # sleep(2)

    lang_code = translation.get_language()
    comments_to_dict = [comment.to_dict(lang=lang_code) for comment in comments]
    return _generate_response(request, comments_to_dict)

