# -*- coding: utf-8 -*-
import urllib2
import urllib
import os
import StringIO
import time
import json
test_img = os.path.join(os.path.dirname(__file__),'python.png')
print test_img

def _encode_multipart_formdata(fields, files):
    body = StringIO.StringIO()
    BOUNDARY = '----------%s' % time.time()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        body.write('--' + BOUNDARY)
        body.write(CRLF)
        body.write('Content-Disposition: form-data; name="%s"' % key)
        body.write(CRLF)
        body.write(CRLF)
        body.write('%s' % value)
        body.write(CRLF)
    for key, file in files.iteritems():
        file.seek(0)
        body.write('--' + BOUNDARY)
        body.write(CRLF)        
        body.write('Content-Disposition: form-data; name="image"; filename="%s"' % (key)) # filename.split('/')[-1]
        body.write(CRLF)        
        body.write('Content-Type: application/octet-stream')
        body.write(CRLF)
        body.write(CRLF)
        body.write(file.read())
        body.write(CRLF)
    body.write('--' + BOUNDARY + '--')
    body.write(CRLF)
    body.write(CRLF)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body.getvalue()


def test_add_point(uid):
    data = {'uid': str(uid),
            'title': 'title',
            'type': 'shop',
            'description': 'test description',
            'coordinates': '[53.88988, 27.591129]',
            'address': 'st. 53',
            }
    files = {'python.png': file(test_img), 'python1.png': file(test_img)}
    content_type, body = _encode_multipart_formdata(data.iteritems(),
                                                    files)
    req = urllib2.Request('http://localhost:8080/api/point/add', body,
                          headers={'Content-Type': content_type,}
                          )
    response = urllib2.urlopen(req)
    print response.read()


def init_app():
    response = urllib2.urlopen('http://localhost:8080/api/init', '')
    res = response.read()
    print "INIT %s " % res
    global UID
    UID = json.loads(res)['uid']

def get_points():
    print urllib2.urlopen('http://localhost:8080/api/points').read()

def get_messages(UID):
    print urllib2.urlopen('http://localhost:8080/api/messages?uid=%s' % UID).read()

def change_message(UID, mid):
    print urllib2.urlopen('http://localhost:8080/api/messages/read', urllib.urlencode({'uid': UID, 'id': mid})).read()

def update_point(UID):
    print urllib2.urlopen('http://localhost:8080/api/point/offer', urllib.urlencode({'uid': UID, 'id': 1, 'description': "TEST"})).read()

    
#uid = "ce625f7ff4ddd20e0d5f171d085b68a7"
UID = "93e71af0d36f45de941a5ce377c9cda7"

#print "INIT"
#init_app()
print "POINTS"
get_points()
print "ADD POINT"
test_add_point(UID)
print "GET MESSAGES"
get_messages(UID)
print "CHANGE MESSAGES"
change_message(UID, 5)
print "UPDATE POINT"
update_point(UID)

