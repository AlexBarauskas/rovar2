from django import template
from django.conf import settings
import json
from os import path

register = template.Library()


class CompressCssJs(template.Node):
    def __init__(self, name):
        super(CompressCssJs, self).__init__()
        self.url = '/static/'
        self.type = name

    def render(self, context):
        conf = json.loads(open(path.join(settings.PROJECT_ROOT,
                                         'Gruntfile.json')).read())
        src = conf.get(self.type)
        if src is None:
            return ''
        if not settings.DEBUG:
            files = [src['out']]
        else:
            files = ['/' + '/'.join(i.split('/')[1:]) for i in src['in']]
        if self.type == 'js':
            template_str = '<script src="%s"></script>\n'
        elif self.type == 'css':
            template_str = '<link type="text/css" href="%s" rel="stylesheet"/>\n'
        else:
            return ''
        html_data = ''
        for f in files:
            html_data += template_str % f
        return html_data.strip('\n')


def get_path_from_tokens(token):
    tokens = token.split_contents()
    if len(tokens) > 1:
        return tokens[1]
    else:
        return None


def compress_url_tag(parser, token):
    return CompressCssJs(get_path_from_tokens(token))
register.tag('grunt', compress_url_tag)
