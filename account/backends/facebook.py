# -*- coding: utf-8 -*-
import cgi
import json
import urllib

from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from account.backends import DenyException


class FacebookBackend():
    key       = settings.ACCOUNT_FACEBOOK_KEY
    secret    = settings.ACCOUNT_FACEBOOK_SECRET
    name      = 'facebook'
    title     = 'Facebook'

    def get_auth_url(self, return_to=None):
        print return_to
        args = { 'client_id' : self.key,
                 'redirect_uri'  : return_to,
                 'scope' : '' }
        url = "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(args)
        return (None, url)

    def get_token(self, request, redirect_url=None):
        try:
            code = request.GET['code']
        except MultiValueDictKeyError:
            if request.GET['error'] and request.GET['error'] == 'access_denied':
                raise DenyException('Access dennied by user')
        args = { 'client_id'  : self.key,
                 'redirect_uri' : redirect_url,
                 'client_secret' : self.secret,
                 'code' : code}
        url = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args)
        
        data = cgi.parse_qs(urllib.urlopen(url).read())
        print data
        return data["access_token"][-1]

    def serialize(self, token):
        return token.to_string()

    def deserialize(self, db_token):
        return OAuthToken.from_string(db_token)

    def get_user_data(self, access_token):
        args = { 'access_token': access_token}
        url = 'https://graph.facebook.com/me?' + urllib.urlencode(args)
        user_info = json.loads(urllib.urlopen(url).read())
        return { 'id' : user_info['id'],
                 'name': user_info.get('name', ''),
                 'link': user_info.get('link', ''),
                 'screen_name': user_info.get('username', ''),
                 'picture':'http://graph.facebook.com/%s/picture/' % user_info['id'],
                 'backend': 'facebook',
            }

    
