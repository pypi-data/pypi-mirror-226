# standard imports
import unittest
import logging
import os

# local imports
from usumbufu.client.pgp import PGPClientSession

# testutil imports
from tests.base import TestBaseAuth


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestPGPClient(TestBaseAuth):

    def setUp(self):
        super(TestPGPClient, self).setUp()
        pk_export_file = os.path.join(self.data_dir, 'pgp', 'privatekeys.asc')
        f = open(pk_export_file, 'r')
        pk_export = f.read()
        f.close()
        self.session = PGPClientSession('http://localhost:8080', pk_export, passphrase='merman')
        self.challenge = 'challenge="deadbeef",max-age="60",realm="foo"'


    def test_sign_challenge(self):
        c = self.session.process_auth_challenge(self.challenge, method='HOBA')


if __name__ == '__main__':
    unittest.main()
