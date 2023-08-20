# standard imports
import logging
import tempfile
import os
import shutil

# external imports
import gnupg

# local imports
from usumbufu.error import (
        AuthenticationError,
        AlienMatterError,
        )
from .base import Filter

logg = logging.getLogger(__name__)


class PGPFilter(Filter):

    default_name = 'pgp filter'

    def __init__(self, trusted_keys, fetcher, gnupg_home=None, decrypt_on_decode=True):
        super(PGPFilter, self).__init__()
        self.gnupg_home = gnupg_home
        self.gnupg_is_temp = False
        if self.gnupg_home == None:
            self.gnupg_home = tempfile.mkdtemp()
            self.gnupg_is_temp = True
        else:
            os.makedirs(gnupg_home, exist_ok=True)
        self.gpg = gnupg.GPG(gnupghome=gnupg_home)
        self.trusted_keys = trusted_keys
        self.auth_keys = []
        self.fetcher = fetcher
        self.decrypt_on_decode = decrypt_on_decode
       

    def __del__(self):
        if self.gnupg_is_temp:
            shutil.rmtree(self.gnupg_home)


    def verify(self, data_in, signature=None, require_trust=False):
        data = data_in
        if isinstance(data, str):
            data = data.encode('utf-8')
        if signature != None:
            (h, tmp_signature) = tempfile.mkstemp()
            f = open(tmp_signature, 'wb')
            f.write(signature)
            f.close()

            r = self.gpg.verify_data(tmp_signature, data) #.encode('utf-8'))
            os.unlink(tmp_signature)
            logg.debug('verify detached {}'.format(r.status))
        else:
            r = self.gpg.verify(data)
            logg.debug('verify embedded {}'.format(r.status))
        logg.debug('signature result {} {} {} {}'.format(r.valid, r.status, r.fingerprint, r.trust_text))
        if not r.valid:
            logg.error('invalid signature with fingerprint: {}'.format(r.fingerprint))
            return None
        if require_trust:
            # unfortunately this does not seem to work,
            #if r.trust_level >= r.TRUST_FULLY:
            if not r.fingerprint in self.trusted_keys:
                logg.error('trust requirement not met for {}'.format(r.fingerprint))
                return None
        return r.fingerprint


    def import_keys(self, v, signature_v=None):
        export = self.fetcher.get(v) # notice: this can be a regular usumbufu.retrieve.Fetcher
        export_keys = None
        signature = None
        if signature_v == None:
            export_keys = self.gpg.decrypt(export).data
        else:
            signature = self.fetcher.get(signature_v)
            export_keys = export
        import_result = self.gpg.import_keys(export_keys)
        self.__process_import_trust(import_result)
        if not self.verify(export, signature=signature, require_trust=True):
            raise AlienMatterError('pgp public key bundle')
        self.__process_imports(import_result)


    def __process_import_trust(self, import_result):
        for k in import_result.results:
            logg.debug('trust check {}'.format(k))
            if k['fingerprint'] in self.trusted_keys:
                logg.info('key {} has been given full trust'.format(k['fingerprint']))
                self.gpg.trust_keys(k['fingerprint'], 'TRUST_FULLY')


    def __process_imports(self, import_result):
        for k in import_result.results:
            if k['fingerprint'] == None:
                logg.debug('skipping invalid auth key')
                continue
            logg.info('imported auth pgp key {}'.format(k['fingerprint']))
            self.auth_keys.append(k['fingerprint'])


    def decrypt(self, v):
        return self.gpg.decrypt(v).data


    def decode(self, requester_ip, v, signature=None, identity=None):
        fp = self.verify(v, signature=signature, require_trust=False)
        logg.debug('fp {}'.format(fp))
        if not fp:
            raise AuthenticationError()
        if fp not in self.auth_keys: # would perhaps be better with marginal/full trust check, but it does not seem to work
            logg.error('fingerprint {} not in auth keys'.format(fp))
            raise AuthenticationError('fingerprint {} not in auth keys'.format(fp))
        fp = bytes.fromhex(fp)
        if self.decrypt_on_decode:
            plain_text = self.decrypt(v) 
            if (len(plain_text) > 0 ):
                return (plain_text, signature, fp)
        return (v, signature, fp)
