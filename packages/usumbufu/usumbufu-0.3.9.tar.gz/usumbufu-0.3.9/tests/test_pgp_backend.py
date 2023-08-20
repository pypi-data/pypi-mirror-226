# standard imports
import unittest
import logging
import os

# local imports
from usumbufu.retrieve import Fetcher

# testutil imports
from tests.base import TestPGPBaseAuth


logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()




class TestPGPDecoder(TestPGPBaseAuth):
        
    def test_pgp_embedded(self):
        self.pgp_decoder.import_keys('auth_embedded.asc.asc')


    def test_pgp_detached(self):
        self.pgp_decoder.import_keys('auth.asc', 'auth.asc.asc')


if __name__ == '__main__':
    unittest.main()
