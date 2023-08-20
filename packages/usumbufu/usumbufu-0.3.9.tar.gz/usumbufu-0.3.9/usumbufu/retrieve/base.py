# standard imports
import logging

# local imports
from usumbufu.error import AuthenticationError

logg = logging.getLogger(__name__)


class Fetcher:

    default_name = 'echo fetcher'

    def __init__(self, name=None):
        self.name = name or self.default_name


    def get(self, auth_string):
        return auth_string


    def __str__(self):
        return self.name


class Retriever:

    def __init__(self, name=None):
        self.decoders = []


    def add_decoder(self, decoder):
        self.decoders.append(decoder)


    def load(self, requester_ip, v, signature=None):
        logg.debug('executing retriever "{}" for key {}'.format(str(self), v))
        return self.decode(requester_ip, v, signature=signature)


    def decode(self, requester_ip, v, signature=None, identity=None):
        logg.debug('v started as {} {}'.format(v, type(v)))
        for d in self.decoders:
            logg.debug('applying decoder "{}" for request from ip {}'.format(str(d), requester_ip))
            o = None
            try:
                o = d.decode(requester_ip, v, signature=signature, identity=identity)
            except AuthenticationError as e:
                logg.error('retriever {} bailing after receiving authentication error from {}: {}'.format(str(self), str(d), str(e)))
                return None
            logg.debug('o {} {}'.format(o, type(o)))
            if o == None:
                logg.debug('retriever {} bailing after receiving empty response from {}'.format(str(self), str(d)))
                raise ValueError("Retriever decode returned None")
            v = o[0]
            signature = o[1]
            identity = o[2]
            logg.debug('v is now {} {} identity {}'.format(v, type(v), identity))
        return (v, identity)
