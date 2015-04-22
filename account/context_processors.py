# -*- coding: utf-8 -*-
# @TODO удалить файл

# from account.models import User
# from django.core.exceptions import ObjectDoesNotExist
#
#
# def get_user(request):
#     if request.user and request.user.is_authenticated():
#         try:
#             account = request.user
#         except ObjectDoesNotExist:
#             account = None
#         return {'user': account}
#     return {'user': None}
#