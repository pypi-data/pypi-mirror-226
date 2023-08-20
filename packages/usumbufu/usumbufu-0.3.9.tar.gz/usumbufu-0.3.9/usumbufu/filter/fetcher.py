# standard imports
import logging

# local imports
from usumbufu.retrieve import Fetcher
from .base import Filter

logg = logging.getLogger(__name__)


class FetcherFilter(Fetcher, Filter):

    default_name = 'fetcher filter'

    def __init__(self, fetcher, name=None):
        if name == None:
            name = '{} ({})'.format(FetcherFilter, str(fetcher))
        super(FetcherFilter, self).__init__(name=name)
        self.fetcher = fetcher


    def decode(self, requester_ip, v, signature=None, identity=None):
        logg.debug('getting {}'.format(v))
        return (self.fetcher.get(v), signature, identity)
