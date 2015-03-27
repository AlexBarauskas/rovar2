import api.views as api
import types

def _parse_doc(s):
    res = []
    cur_tag = None
    el = None
    for l in s.split('\n'):
        l = l.strip()
        if l.startswith('--'):
            tag = 'h2'
            l = l[2:]
        elif l.startswith('-'):
            tag = 'h1'
            l = l[1:]
        elif l.startswith('{') or l.startswith('['):
            tag = 'pre'
        elif l.startswith('}') or l.startswith(']'):
            el.append(l)
            l = ''
            tag = 'p'
        elif l.startswith('POST') or l.startswith('GET'):
            tag = 'pre1'
        elif cur_tag == 'pre':
            tag = 'pre'
        else:
            tag = 'p'
        if(tag != cur_tag or tag=='pre1'):
            if el is not None:
                data = '<br/>'.join([s for s in el if s])
                res.append("<%(tag)s>%(data)s</%(tag)s>" % {'data': data,
                                                            'tag': cur_tag})
            if tag=='pre1':
                data = l.replace('<', '&lt;').replace('>', '&gt;')
                res.append("<%(tag)s>%(data)s</%(tag)s>" % {'data': data,
                                                            'tag': 'pre'})
                cur_tag = 'p'
                el = []
            else:
                cur_tag = tag
                el = [l]

        else:
            el.append(l)
    if el is not None:
        data = '<br/>'.join([s for s in el if s])
        res.append("<%(tag)s>%(data)s</%(tag)s>" % {'data': data,
                                                    'tag': cur_tag})
    return res
        

def make_api_doc():
    #functions = [a for a in [api.__getattribute__(_a) for _a in dir(api)] if type(a) == types.FunctionType and a.__doc__ and a.__module__ == 'api.views']
    #print [f.__name__ for f in functions]
    functions = ['initialize_app',
                 'locations', 'location',
                 'get_types',
                 'points', 'tracks',
                 'add_point', 'point_offer',
                 'messages', 'message_read',
                 ]
    docs = [api.__getattribute__(_a).__doc__ for _a in functions]
    return [_parse_doc(d) for d in docs]



