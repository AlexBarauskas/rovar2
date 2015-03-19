from xml.dom.minidom import parseString
import time

class XMLTrack(object):
    name = ''
    dom = None
    track = None
    lat = 'lat'
    lon = 'lon'
    type = None

    def __init__(self, xml_string):
        if xml_string.find('kml') >= 0:
            self.type = 'kml'
        self.dom = parseString(xml_string)    

    def get_track(self):
        if self.type == 'kml':
            return self.get_track_kml()
        self.track = {}
        track_node = self.dom.getElementsByTagName('trk')[0]
        self.track["name"] = track_node.getElementsByTagName('name')[0].firstChild.nodeValue
        track_points = track_node.getElementsByTagName('trkpt')
        self.track['rout'] = []
        for p in track_points:
            try:
                ele = float(p.getElementsByTagName('ele')[0].childNodes[0].data)
            except:
                ele = 0
            try:
                t = p.getElementsByTagName('time')[0].childNodes[0].data
                t = time.mktime(time.strptime(t, '%Y-%m-%dT%H:%M:%SZ'))
            except:
                t = 0

            self.track['rout'].append((float(p.getAttribute(self.lat)),
                                       float(p.getAttribute(self.lon)),
                                       t, ele
                                       ))
        return self.track

    def get_track_kml(self):
        self.track = {}
        #track_node = self.dom.getElementsByTagName('trk')[0]
        self.track["name"] = '' #track_node.getElementsByTagName('name')[0].firstChild.nodeValue
        #track_points = track_node.getElementsByTagName('trkpt')
        self.track['rout'] = []
        #for p in track_points:
        #    self.track['rout'].append((float(p.getAttribute(self.lat)),
        #                                 float(p.getAttribute(self.lon))))
        coordinats = self.dom.getElementsByTagName('coordinates')[0].firstChild.nodeValue
        coordinats = coordinats.split(' ')
        for i in coordinats:
            p = i.split(',')[:2]
            #p.reverse()
            self.track['rout'].append([float(p[1]),
                                       float(p[0])])
        return self.track
    

if __name__ == '__main__':
    import sys
    if len(sys.argv)>1:
        t = XMLTrack(file(sys.argv[1]).read())
        #print t._find_by_tag_name('trkpt')
        print t.get_track()
