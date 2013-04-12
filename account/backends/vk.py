# -*- coding: utf-8 -*-
from django.conf import settings
from oauth.oauth import OAuthToken

from account.backends import DenyException
from django.utils.datastructures import MultiValueDictKeyError

import json
import urllib

class VkBackend():
    key       = settings.ACCOUNT_VK_KEY
    secret    = settings.ACCOUNT_VK_SECRET
    name      = 'vk'
    title     = 'Vkontakte'

    def get_auth_url(self, return_to=None):
        args = { 'client_id' : self.key,
                 'redirect_uri'  : return_to,
                 'scope' : 'wall',
                 'response_type' : 'code',
                 }
        return (None,
                "http://api.vk.com/oauth/authorize?" + urllib.urlencode(args)
                )

    def get_token(self, request, redirect_url=None):
        try:
            code = request.GET['code']
        except MultiValueDictKeyError:
            if request.GET['error']:
                raise DenyException('Access dennied by user')
        #
        db_request_token = request.session.get('account_token','')
        args = { 'client_id'  : self.key,
                 'redirect_uri' : redirect_url,
                 'client_secret' : self.secret,              
                 'code' : code,
                 'format' : 'json',
                 }

        url = "https://api.vk.com/oauth/access_token?" + urllib.urlencode(args)
        urllib._urlopener = urllib.FancyURLopener()
        urllib._urlopener.addheader('Connection', 'close')
        data = urllib.urlopen(url)
        data = json.loads(data.read())
        return data['access_token']

    def serialize(self, token):
        return token.to_string()

    def deserialize(self, db_token):
        return OAuthToken.from_string(db_token)

    def get_user_data(self,access_token):
        param={'access_token': access_token,
               'fields': 'nickname, screen_name, uid, photo',
               }
        url='https://api.vk.com/method/users.get?'+urllib.urlencode(param)
        user_info = json.loads(urllib.urlopen(url).read())['response'][0]
        return { 'id': user_info.get('uid',''),
                 'name': '%s %s' % (user_info.get('first_name',''),
                                    user_info.get('last_name',''),
                                    ),
                 'screen_name': user_info.get('screen_name',''),
                 'picture': user_info.get('photo',None),
                 'link': '//vk.com/%s' % user_info.get('vuid',''),
                 'backend': 'vk',
                 }
