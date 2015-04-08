# from account.models import Account
# from django.core.exceptions import ObjectDoesNotExist
#
def get_account(request):
    return {}
#     if request.user and request.user.is_authenticated():
#         try:
#             account = request.user.account_set.get() #get_profile()
#         except ObjectDoesNotExist:
#             user = request.user
#             account = Account(user=user, name='%s %s' % (user.first_name,
#                                                          user.last_name))
#             account.save()
#         return {'account' : account}
#     return {'account' : None}
