# standard imports
import unittest
import logging
import os
import datetime

# external imports
from http_hoba_auth import Hoba

# local imports
from usumbufu.filter.util import source_hash
from usumbufu.challenge import Challenger
from usumbufu.filter import Filter
from usumbufu.filter.hoba import HobaFilter
from usumbufu.filter.sha256 import SHA256Filter
from usumbufu.retrieve import Retriever
from usumbufu.filter.util import source_hash
from usumbufu.retrieve import Fetcher
from usumbufu.filter.fetcher import FetcherFilter
from usumbufu.error import ChallengeError

# testutil imports
from tests.base import TestBaseAuth

script_dir = os.path.realpath(os.path.dirname(__file__))

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestChallengeAuth(TestBaseAuth):
    def setUp(self):
        self.challenger = Challenger()


    def test_clear(self):
        one_ip = '127.0.0.1'
        two_ip = '192.168.0.100'

        (one_k, one_exp) = self.challenger.request(one_ip)
        (two_k, two_exp) = self.challenger.request(two_ip)
        self.assertEqual(self.challenger.get(one_ip, one_k), one_k) 
        self.assertEqual(self.challenger.get(two_ip, two_k), two_k) 

        self.challenger.clear(one_ip, one_k)
        self.assertEqual(self.challenger.get(two_ip, two_k), two_k) 
        with self.assertRaises(ChallengeError):
            self.assertEqual(self.challenger.get(one_ip, one_k), one_k) 


    def test_clear_serial(self):
        one_ip = '127.0.0.1'
        two_ip = '192.168.0.100'

        (one_k, one_exp) = self.challenger.request(one_ip)
        self.challenger.clear(one_ip, one_k)
        (two_k, two_exp) = self.challenger.request(two_ip)
        self.assertEqual(self.challenger.get(two_ip, two_k), two_k) 


    def test_ip_check(self):
        one_ip = '127.0.0.1'
        two_ip = '192.168.0.100'

        (one_k, one_exp) = self.challenger.request(one_ip)
        with self.assertRaises(ChallengeError):
            self.challenger.get(two_ip, one_k)


    def test_expire_check(self):
        one_ip = '127.0.0.1'

        (one_k, one_exp) = self.challenger.request(one_ip)
        internal_key = source_hash(one_ip, one_k)
        self.challenger.challenges[internal_key].expires = datetime.datetime.fromtimestamp(1)
        with self.assertRaises(ChallengeError):
            self.challenger.get(one_ip, one_k)


if __name__ == '__main__':
    unittest.main()
