# standard imports
import unittest
import logging
import os
import urllib

# local imports
from usumbufu.client import (
    split_auth_header,
    split_challenge_header,
    )
from usumbufu.client.base import (
        ClientSession,
        BaseTokenStore,
        )

# testutil imports
from tests.base import TestBaseAuth

script_dir = os.path.realpath(os.path.dirname(__file__))

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestClient(TestBaseAuth):

    def setUp(self):
        self.token_store = BaseTokenStore()
        self.session = ClientSession('http://localhost:5555', token_store=self.token_store)


    def test_hello(self):
        logg.debug(self.session)


    def test_set_token(self):
        rq = urllib.request.Request('http://localhost:5555')
        self.session.set_token(rq, 'deadbeef')


    def test_auth_header(self):
        h = 'challenge="asf",max-age="33",realm="foo"'
        o = split_auth_header(h)
        self.assertEqual(o.get('challenge'), 'asf')
        self.assertEqual(o.get('max-age'), '33')
        self.assertEqual(o.get('realm'), 'foo')


    def test_challenge_header(self):
        h = 'challenge="asf",max-age="33",realm="foo"'
        o = split_challenge_header(h)

        h = 'challenge="asf"'
        with self.assertRaises(ValueError):
            o = split_challenge_header(h)
        o = split_challenge_header(h, strict=False)


if __name__ == '__main__':
    unittest.main()
