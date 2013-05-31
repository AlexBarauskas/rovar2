from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
import json

#from tmp.parse_xml import XMLTrack
from manager.models import Track
import json

def get_available_tracks(request):
    state = '0'
    tracks = Track.objects.filter(state__lte=state)
    tracks = [t.id for t in tracks]
    
    return HttpResponse(json.dumps({'ids': tracks}),
                        mimetype='text/json')
    

def track(request, track_id=None):
    kwargs = {}
    if track_id:
        kwargs['id'] = track_id
    try:
        t = Track.objects.get(**kwargs)
        track = {'route': json.loads(t.coordinates),
                 'title': t.name,
                 'description': t.description,
                 'video': t.video or '',
                 'id': t.id}
    except:
        track = {'route': [[0,0],[0,0]]}
    return HttpResponse(json.dumps(track),
                        mimetype='text/json')
