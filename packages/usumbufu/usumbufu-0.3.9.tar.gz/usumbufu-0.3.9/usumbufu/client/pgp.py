# standard imports
import logging
import tempfile
import shutil

# extended imports
import gnupg

# local imports
from usumbufu.client.hoba import HobaClientSession

logg = logging.getLogger(__name__)


class PGPClientSession(HobaClientSession):

    alg = '969'

    def __init__(self, origin, private_key=None, fingerprint=None, passphrase=None, gpg_dir=None, token_store=None):
        self.origin = origin
        self.actual_gpg_dir = gpg_dir
        self.pgp_is_temp = False
        if self.actual_gpg_dir == None:
            self.actual_gpg_dir = tempfile.mkdtemp()
            self.pgp_is_temp = True
        logg.info('using gpg dir {}'.format(self.actual_gpg_dir))
        self.gpg = gnupg.GPG(gnupghome=self.actual_gpg_dir)
        self.fingerprint = None
        if private_key != None:
            import_result = self.gpg.import_keys(private_key)
            self.fingerprint = import_result.results[0]['fingerprint']
            if import_result.sec_read == 0:
                raise ValueError('Export bundle contained no private keys')
            elif gpg_dir == None and import_result.sec_imported > 1:
                logg.warning('multiple private keys found. key with fingerprint {} will be used to sign challenges'.format(self.fingerprint))
        elif fingerprint != None:
            self.fingerprint = fingerprint
            #NotImplementedError('currently only works with passed private key export blobs')
        self.passphrase = passphrase


    def __del__(self):
        if self.pgp_is_temp:
            shutil.rmtree(self.actual_gpg_dir)


    def sign_auth_challenge(self, plaintext, hoba, encoding):
        r = self.gpg.sign(plaintext, passphrase=self.passphrase, detach=True)
        
        if encoding == 'base64':
            r = r.data

        hoba.signature = r
        return str(hoba)


    def __str__(self):
        return 'pgp'
