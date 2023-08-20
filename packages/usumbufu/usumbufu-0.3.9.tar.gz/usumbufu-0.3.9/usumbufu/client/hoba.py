# standard imports
import logging
import base64

# external imports
from http_hoba_auth import Hoba

# local imports
from usumbufu.client.base import challenge_nonce
from usumbufu.client.util import get_header_parts

logg = logging.getLogger(__name__)


class HobaClientSession:

    def hoba_kid(self, encoding='base64'):
        kid = None
        #if encoding == 'base64':
        #    b = bytes.fromhex(self.fingerprint)
        #    kid = base64.b64encode(b)
        kid = bytes.fromhex(self.fingerprint)
        return kid 


    def process_auth_request(self, request):
        return request
        
 
    def process_auth_challenge(self, header, encoding='base64', method='HOBA'):
        if method != 'HOBA':
            logg.error('only HOBA implemented for pgp handler client, got {}'.format(method))
            return None

        o = get_header_parts(header)
        c = o['challenge']
        if encoding == 'base64':
            c = base64.b64decode(o['challenge'])
        elif encoding != None:
            NotImplementedError(encoding)
       
        hoba = Hoba(self.origin, o['realm'])
        hoba.challenge = c
        hoba.nonce = challenge_nonce()
        hoba.kid = self.hoba_kid()
        hoba.alg = self.alg
        
        plaintext = hoba.to_be_signed()

        return self.sign_auth_challenge(plaintext, hoba, encoding)


    def sign_auth_challenge(self, plaintext, hoba, encoding):
        raise NotImplementedError('challenge signing must be implemented')
