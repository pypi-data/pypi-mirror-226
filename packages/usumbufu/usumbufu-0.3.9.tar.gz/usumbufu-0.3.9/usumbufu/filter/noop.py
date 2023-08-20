# local imports
from .base import Filter


class NoopFilter(Filter):
  
    default_name = 'noop filter'

    def decode(self, requester_ip, v, signature=None, identity=None):
        return (v, signature, identity)
