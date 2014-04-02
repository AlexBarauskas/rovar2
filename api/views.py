# -*- coding: utf-8 -*-
"""@package api
    Documentation for this module.
     
    More details.
"""
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.conf import settings
import json

from map.models import Track, Point, Type

#http://blogs.cs.st-andrews.ac.uk/jfdm/2013/04/04/documenting-python-using-doxygen/

def points(request):
    '''
    Получение информации о доступных точках.
    /api/points?page=P&per_page=N
GET-запрос может не содержать параметров.
В случае отсутствия параметра page или не верного преобразования в целочисленное значение, будет возвращен список всех доступных точек.
В случае отсутствия или неврно указанного параметра per_page значение по умолчанию принимается 10.
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
    if page is not None
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
