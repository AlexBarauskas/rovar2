from django.contrib.auth.models import User


class SocialLoginBackend():
    def authenticate(self, username=None, password=None): 
        try:
            if password == 2:
                return User.objects.get(username=username)  
        except:  
            pass  
        return None

    def get_user(self, user_id):  
        try:  
            return User.objects.get(pk=user_id)  
        except:  
            return None

