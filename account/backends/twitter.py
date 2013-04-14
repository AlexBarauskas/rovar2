# -*- coding: utf-8 -*-
from django.conf import settings
from oauth.oauth import OAuthToken
from _twitter.oauthtwitter import OAuthApi

from account.backends import DenyException
#     BackendBase, BackendType, RecoverableError
                              
from django.utils.datastructures import MultiValueDictKeyError


class TwitterBackend():
    key       = settings.ACCOUNT_TWITTER_KEY
    secret    = settings.ACCOUNT_TWITTER_SECRET
    name      = 'twitter'
    title     = 'Twitter'

    def get_auth_url(self, return_to=None):
        api = OAuthApi(self.key, self.secret)
        request_token = api.getRequestToken(callback=return_to,
                                            access='read')
        token = self.serialize(request_token)
        auth_url = api.getAuthorizationURL(request_token)
        return (token, auth_url)

    def get_token(self, request, redirect_url=None):
        try:
            verifier = request.GET['oauth_verifier']
        except MultiValueDictKeyError:
            if request.GET['denied']:
                raise DenyException('Access dennied by user')

        db_request_token = request.session.get('account_token','')
        request_token = self.deserialize(db_request_token)
        api = OAuthApi(self.key, self.secret, request_token)
        access_token = api.getAccessToken(verifier=verifier)
        return access_token

    def serialize(self, token):
        return token.to_string()

    def deserialize(self, db_token):
        return OAuthToken.from_string(db_token)

    def get_user_data(self,access_token):
        api = OAuthApi(self.key, self.secret, access_token)
        try:
            user_info = api.GetUserInfo()
        except:
            return None
        
        friends = api.GetFollowers()
        friends = [f.GetId() for f in friends]
        
        return { 'id': user_info.get('id',''),
                 'name': user_info.get('name','') or user_info.get('screen_name',''),
                 'screen_name': user_info.get('screen_name',''),
                 'picture': user_info.get('profile_image_url',None),
                 'link': '//twitter.com/%s' % user_info.get('screen_name',''),
                 'backend': 'twitter',
                 }
