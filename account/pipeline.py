# -*- coding: utf-8 -*-
from django.shortcuts import redirect

from social.pipeline.partial import partial
from account.models import User

# @partial
# def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
#     if kwargs.get('ajax') or user and user.email:
#         return
#     elif is_new and not details.get('email'):
#         email = strategy.request_data().get('email')
#         if email:
#             details['email'] = email
#         else:
#             return redirect('require_email')


def save_profile(backend, user, response, *args, **kwargs):
    """
    Функция вытягивания данных о пользователи из соц сети.
    user - account.models.User уже в сессии
    response - Ответ от OAuth сервера авторизации
    """
    if backend.name == 'facebook':
        user.first_name = response.get('first_name')
        user.last_name = response.get('last_name')
        user.gender = response.get('gender')
        user.save()
    if backend.name == 'twitter':
        details = kwargs.get('details')
        user.first_name = details.get('first_name')
        user.last_name = details.get('last_name')
        user.save()
    if backend.name == 'vkontakte':
        # @TODO найти у кого есть контактик и заполнить поля
        # user.first_name = response.get('first_name')
        # user.last_name = response.get('last_name')
        # user.gender = response.get('gender')
        user.save()
