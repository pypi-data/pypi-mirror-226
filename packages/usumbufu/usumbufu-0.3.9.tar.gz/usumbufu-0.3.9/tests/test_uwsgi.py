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
from usumbufu.adapters.uwsgi import (
        UWSGIHTTPAuthorization,
        UWSGIAdapter,
        )
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


class TestUWSGIAuth(TestBaseAuth):
    def test_http_err_uwsgi(self):
        auth_string = 'Bearer Zm9vYmFyYmF6Cg=='
        realm = 'foorealm'
        client_id = 'barclient'
        origin = 'http://localhost'
        ip = '127.0.0.1'

        retriever = Retriever()
        retriever.add_decoder(ArghFilter())
        env = {
            'HTTP_AUTHORIZATION': auth_string,
                }
        auther = UWSGIHTTPAuthorization(retriever, env, realm, client_id=client_id, origin=origin)
        with self.assertRaises(AuthenticationError):
            auther.check()

        auth_vector = UWSGIAdapter()
        auth_vector.register(auther)
        auth_vector.activate(auther.component_id)
        r = auth_vector.check()
        self.assertIsNone(r)


if __name__ == '__main__':
    unittest.main()
