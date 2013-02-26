from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
import json

from tmp.parse_xml import XMLTrack

def track(request):
    #track=[[0,0],[32,60]]

    t = XMLTrack(open("tmp/GPSLogMee_Log_1_141.txt").read())
    track = t.get_track()

    return HttpResponse(json.dumps(track),
                        content_type="text/json")
