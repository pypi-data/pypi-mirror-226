# standard imports
import logging

# external imports
from http_hoba_auth import Hoba

# local imports
from .base import Filter
from .util import source_hash

logg = logging.getLogger(__name__)


class HobaFilter(Filter):

    default_name = 'hoba filter'
    
    def __init__(self, origin, realm, challenge_store, alg='00', name=None):
        super(HobaFilter, self).__init__(name=name)
        self.origin = origin
        self.realm = realm
        self.challenge_store = challenge_store
        self.alg = alg


    def decode(self, requester_ip, v, signature=None, identity=None):
        hoba = Hoba(self.origin, self.realm, alg=self.alg)
        hoba.parse(v)

        challenge_check = self.challenge_store.get(requester_ip, hoba.challenge)

        if challenge_check != hoba.challenge:
            #logg.error('challenge mismatch {} != {}'.format(self.challenge.hex(), s.hex()))
            logg.error('challenge mismatch {} != {}'.format(challenge_check, v))
            raise ValueError('challenge mismatch')
        tbs = hoba.to_be_signed()
        logg.debug('hoba filter {} -> {}'.format(v, tbs))
        if signature == None:
            signature = hoba.signature
        if identity == None:
            identity = hoba.kid
        return (tbs.encode('utf-8'), signature, identity)
