def manager_menu_item(request):
    t = request.path.strip('/').split('/')
    #print t
    menu_item = None
    items = ['types', 'tracks', 'points', 'moderation']
    if len(t)>1 and t[0] == 'manager' and t[1] in items:
        menu_item = t[1]
    return {'menu_item': menu_item}


from api.models import Message
from map.models import Location
def moderation_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {'number_moderation': Message.objects.filter(state='m',
                                                            point__location__id__in=[i[0] for i in Location.objects.filter(admins=request.user).values_list('id')]).count()}
    else:
        return {'number_moderation': 0}
