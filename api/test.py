# -*- coding: utf-8 -*-
import urllib2
import urllib
import os
import StringIO
import time
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


def test_add_point():
    uid = "ce625f7ff4ddd20e0d5f171d085b68a7"
    data = {'uid': uid,
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

test_add_point()
