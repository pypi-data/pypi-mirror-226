# standard imports
import hashlib

# local imports
from .base import Filter


# applies sha256 on the piped challenge material, like the client does (see client_hoba.py:XORSignerSession.process_auth_challenge)
class SHA256Filter(Filter):

    default_name = 'sha256 filter'

    def decode(self, requester_ip, v, signature=None, identity=None):
        h = hashlib.sha256()
        h.update(v)
        z = h.digest()
        return (z, signature, identity)
