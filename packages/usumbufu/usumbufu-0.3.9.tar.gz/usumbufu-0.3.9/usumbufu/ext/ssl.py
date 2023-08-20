# standard imports
import logging
import hashlib

# third-party imports
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding 
from cryptography.hazmat.primitives.serialization import PublicFormat 

# local imports
from ..auth import Auth


class SSLClient(Auth):
    """Handles authentication through SSL Client certificates.

    The digest value used to retrieve authentication data is the hex value of the certificate's public key.

    The certificate is NOT validated against authority, it is assumed that this is already handled by the HTTP server.
    """
    logger = logging.getLogger(__name__)
    component_id = 'ssl'
 

    """Implements Auth.check
    """
    def check(self):
        self.logger.debug('ssl check {}'.format(self.auth_string))
        crt = x509.load_der_x509_certificate(self.auth_string)
        pubkey = crt.public_key()
        pubkey_serial = pubkey.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
        pubkey_numbers = pubkey.public_numbers()
        pubkey_bytes = pubkey_numbers.n.to_bytes(256, 'big')
        self.logger.info('SSL client cert found with public key {}'.format(pubkey_bytes.hex()))
        h = hashlib.sha256()
        h.update(pubkey_bytes)
        identity = h.digest()
        auth_data = self.retriever.load(identity)
        if auth_data == None:
            return None
        return (self.component_id, identity, auth_data)

    """Implements Auth.method
    """
    def method(self):
        return None
