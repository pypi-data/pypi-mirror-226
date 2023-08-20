# standard imports
import os
import logging
import unittest
import base64

# local imports
from usumbufu.filter import Filter
from usumbufu.filter.noop import NoopFilter
from usumbufu.retrieve import Retriever
from usumbufu.error import AuthenticationError
from usumbufu.ext.http import HTTPAuthorization
from usumbufu.auth import AuthVector

# testutil imports
from tests.base import TestBaseAuth

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, 'testdata')

ip = '127.0.0.1'


class ArghFilter(Filter):

    default_name = 'filter of aaaaargh'

    def decode(self, requester_ip, data, signature=None, identity=None):
        raise RuntimeError('catch this')


class PokeFilter(Filter):

    default_name = 'setme'

    def decode(self, requester_ip, data, signature=None, identity=None):
        self.name = data
        return None


class TestHTTPAuth(TestBaseAuth):

    def test_http_err(self):
        auth_string = 'Bearer Zm9vYmFyYmF6Cg=='
        realm = 'foorealm'
        #origin = 'http://localhost'
        ip = '127.0.0.1'

        retriever = Retriever()
        retriever.add_decoder(ArghFilter())
        auther = HTTPAuthorization(realm, retriever, ip, auth_string)
        with self.assertRaises(AuthenticationError):
            auther.check()

        auth_vector = AuthVector()
        auth_vector.register(auther)
        auth_vector.activate(auther.component_id)
        r = auth_vector.check()
        self.assertIsNone(r)


def test_http_multi(self):
        bearer_value = 'Zm9vYmFyYmF6Cg=='
        auth_string_bearer = 'Bearer ' + bearer_value
        basic_value = 'YmF6OmJhcgo='
        auth_string_basic = 'Basic ' + basic_value
        realm = 'foorealm'
        #origin = 'http://localhost'
        ip = '127.0.0.1'

        one_retriever = Retriever()
        one_filter = PokeFilter()
        one_retriever.add_decoder(one_filter)

        two_retriever = Retriever()
        two_filter = PokeFilter()
        two_retriever.add_decoder(two_filter)

        one_auth = HTTPAuthorization(realm, one_retriever, ip, auth_string_basic)
        two_auth = HTTPAuthorization(realm, two_retriever, ip, auth_string_bearer)

        auth = AuthVector()
        auth.register(one_auth)
        auth.activate(one_auth.component_id)
        auth.register(two_auth)
        auth.activate(two_auth.component_id)

        r = auth.check()
        self.assertIsNone(r)
        self.assertNotEqual(one_filter.name, 'setme')
        self.assertNotEqual(two_filter.name, 'setme')
        self.assertNotEqual(one_filter.name, two_filter.name)


if __name__ == '__main__':
    unittest.main()
