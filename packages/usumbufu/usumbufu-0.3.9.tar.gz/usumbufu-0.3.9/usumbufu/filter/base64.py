# standard imports
import base64

# local imports
from .base import Filter


class Base64Filter(Filter):

    default_name = 'base64 filter'

    def __init__(self, reverse=False, name=None):
        if reverse and name == None:
            name = '{} (reverse)'.format(self.default_name)
        super(Base64Filter, self).__init__(name=name)
        self.reverse = reverse


    def decode(self, requester_ip, v, signature=None, identity=None):
        if self.reverse:
            return (base64.b64encode(v), signature, identity)
        return (base64.b64decode(v), signature, identity)
