# standard imports
import os
import logging
import unittest

# local imports
from usumbufu.filter import Filter
from usumbufu.filter.base64 import Base64Filter
from usumbufu.filter.fetcher import FetcherFilter
from usumbufu.retrieve.file import FileFetcher
from usumbufu.retrieve import Retriever
from usumbufu.error import AuthenticationError

# test imports
from tests.base import TestPGPBaseAuth

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, 'testdata')

ip = '127.0.0.1'

class CommaColonFilter(Filter):

    default_name = 'comma colon bogus decoder'

    def decode(self, requester_ip, data, signature=None, identity=None):
        logg.debug('decode data {} {}'.format(data, type(data)))
        d = {}
        for p in data.split(b','):
            (k, v) = p.split(b':')
            d[k] = v.rstrip()
        return (d, signature, identity)


class NoneFilter(Filter):

    def decode(self, requester_ip, data, signature=None, identity=None):
        raise AuthenticationError()


class RaiseFilter(Filter):

    def decode(self, requester_ip, data, signature=None, identity=None):
        raise AuthenticationError('I am useless')


class TestRetrieve(TestPGPBaseAuth):

    def setUp(self):
        super(TestRetrieve, self).setUp()
        self.acl_dir = os.path.join(data_dir, 'acl')
        self.valid_acl = '01fa52ce-4405-4070-9578-c89815833f8b'
        self.malformed_acl = '10c16ce4-8129-44e4-8eb8-e7a3d7d15080'
        self.trusted_pgp_acl = '42baa113-598c-4223-a98a-6ad4b91b8dc6'
        self.untrusted_pgp_acl = 'ebad25e0-2584-4b84-8a62-002a01ac4380'
        self.fetcher = FileFetcher(self.acl_dir)
        self.fetcher_filter = FetcherFilter(self.fetcher)


    def test_retrieve_file_nodecode(self):
        retriever = Retriever(self.acl_dir) 
        retriever.add_decoder(self.fetcher_filter)
        (v, identity) = retriever.load(ip, self.malformed_acl)
        self.assertEqual(v.rstrip(), b'foo')


    def test_retrieve_file_decode(self):
        retriever = Retriever()
        retriever.add_decoder(self.fetcher_filter)
        retriever.add_decoder(Base64Filter())
        retriever.add_decoder(CommaColonFilter())

        (v, identity) = retriever.load(ip, self.valid_acl)
        self.assertDictEqual(v, {b'foo': b'bar', b'baz': b'xyzzy'})


    def test_retrieve_file_pgpdecode(self):
        self.pgp_decoder.import_keys('auth.asc', 'auth.asc.asc')
        retriever = Retriever()
        retriever.add_decoder(self.fetcher_filter)
        retriever.add_decoder(self.pgp_decoder)
        retriever.add_decoder(Base64Filter())
        retriever.add_decoder(CommaColonFilter())
     
        (v, identity) = retriever.load(ip, self.trusted_pgp_acl)
        self.assertDictEqual(v, {b'foo': b'bar', b'baz': b'xyzzy'})


    def test_retrieve_file_pgpdecode_untrusted(self):
        self.pgp_decoder.import_keys('auth.asc', 'auth.asc.asc')
        retriever = Retriever()
        retriever.add_decoder(self.fetcher_filter)
        retriever.add_decoder(self.pgp_decoder)
    
        o = retriever.load(ip, self.untrusted_pgp_acl)
        self.assertIsNone(o)


    def test_retrieve_file_pgpdecode_detached(self):
        self.pgp_decoder.import_keys('auth.asc', 'auth.asc.asc')
        self.pgp_decoder.decrypt_on_decode = False
        retriever = Retriever()
        retriever.add_decoder(self.fetcher_filter)
        retriever.add_decoder(self.pgp_decoder)
        retriever.add_decoder(Base64Filter())
        retriever.add_decoder(CommaColonFilter())
    
        f = open(os.path.join(self.data_dir, 'acl', self.valid_acl + '.asc'), 'rb')
        signature = f.read()
        f.close()
        (v, identity) = retriever.load(ip, self.valid_acl, signature=signature)
        self.assertDictEqual(v, {b'foo': b'bar', b'baz': b'xyzzy'})


    def test_retrieve_none(self):
        retriever = Retriever()
        retriever.add_decoder(NoneFilter())

        o = retriever.load(ip, b'foo')
        self.assertIsNone(o)


    def test_retireve_exception(self):
        retriever = Retriever()
        retriever.add_decoder(RaiseFilter())

        o = retriever.load(ip, b'foo')
        self.assertIsNone(o)


if __name__ == '__main__':
    unittest.main() 
