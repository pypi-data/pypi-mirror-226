from .api import GleenAI

_default_client = GleenAI()

def set_api_key(key):
    _default_client.set_api_key(key)

def send_message(*args, **kwargs):
    return _default_client.send_message(*args, **kwargs)

