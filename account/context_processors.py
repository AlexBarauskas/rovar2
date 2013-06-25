from account.models import Account

def get_account(request):
    if request.user and request.user.is_authenticated():
        account = request.user.get_profile()
        try:
            account = request.user.get_profile()
        except:
            user = request.user
            account = Account(user=user, name='%s %s' % (user.first_name,
                                                         user.last_name))
            account.save()
        return {'account' : account}
    return {}
