class DenyException(Exception):
    pass

from twitter import TwitterBackend
from vk import VkBackend
from facebook import FacebookBackend

def get_backend(backend_name):
    if backend_name == 'twitter':
        return TwitterBackend()
    if backend_name == 'vk':
        return VkBackend()
    if backend_name == 'facebook':
        return FacebookBackend()
    return None
