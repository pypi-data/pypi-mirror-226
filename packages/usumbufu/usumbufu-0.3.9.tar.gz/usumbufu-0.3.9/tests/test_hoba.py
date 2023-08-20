# standard imports
import unittest
import logging
import os

# external imports
from http_hoba_auth import Hoba

# local imports
from usumbufu.challenge import Challenger
from usumbufu.filter import Filter
from usumbufu.filter.hoba import HobaFilter
from usumbufu.filter.sha256 import SHA256Filter
from usumbufu.retrieve import Retriever
from usumbufu.filter.util import source_hash
from usumbufu.retrieve import Fetcher
from usumbufu.filter.fetcher import FetcherFilter
from usumbufu.error import AuthenticationError

# testutil imports
from tests.base import TestBaseAuth

script_dir = os.path.realpath(os.path.dirname(__file__))

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

ip = '127.0.0.1'
origin = 'http://localhost:5555'
realm = 'foorealm'


class MockVerifierFilter(Filter):
    
    default_name = 'mock verifier filter'

    def decode(self, requester_ip, v, signature=None, identity=None):
        if signature == '\xdd' * 32:
            return ('\xff' * 32, '\xff' * 32,)
        raise AuthenticationError()


class TestHobaAuth(TestBaseAuth):

    def setUp(self):
        self.challenger = Challenger()
        self.hoba_filter = HobaFilter(origin, realm, self.challenger)


    def test_challenge(self):
        (challenge, expire) = self.challenger.request(ip)
        hoba = Hoba(origin, realm)
        hoba.ip = ip
        hoba.challenge = challenge
        hoba.kid = b'\xff' * 32
        hoba.nonce = b'\xee' * 32
        hoba.signature = b'\xdd' * 32

        # noop fetcher to merely echo the 
        fetcher = Fetcher()
        retriever = Retriever()
        retriever.add_decoder(FetcherFilter(fetcher))
        retriever.add_decoder(self.hoba_filter)
        retriever.add_decoder(SHA256Filter())
        retriever.add_decoder(MockVerifierFilter())
        v = retriever.load(ip, str(hoba), hoba.signature)



if __name__ == '__main__':
    unittest.main()
