from xml.dom.minidom import parseString


class XMLTrack(object):
    name = ''
    dom = None
    track = None
    lat = 'lat'
    lon = 'lon'

    def __init__(self, xml_string):
        self.dom = parseString(xml_string)    

    def get_track(self):
        self.track = {}
        track_node = self.dom.getElementsByTagName('trk')[0]
        self.track["name"] = track_node.getElementsByTagName('name')[0].firstChild.nodeValue
        track_points = track_node.getElementsByTagName('trkpt')
        self.track['points'] = []
        for p in track_points:
            self.track['points'].append((p.getAttribute(self.lat),
                                         p.getAttribute(self.lon)))
        return self.track
    

if __name__ == '__main__':
    import sys
    if len(sys.argv)>1:
        t = XMLTrack(file(sys.argv[1]).read())
        #print t._find_by_tag_name('trkpt')
        print t.get_track()
