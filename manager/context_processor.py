def manager_menu_item(request):
    t = request.path.strip('/').split('/')
    #print t
    menu_item = None
    items = ['types', 'tracks', 'points']
    if len(t)>1 and t[0] == 'manager' and t[1] in items:
        menu_item = t[1]
    return {'menu_item': menu_item}
