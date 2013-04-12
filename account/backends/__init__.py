class DenyException(Exception):
    pass

from twitter import TwitterBackend
from vk import VkBackend

def get_backend(backend_name):
    if backend_name == 'twitter':
        return TwitterBackend()
    if backend_name == 'vk':
        return VkBackend()
    return None
