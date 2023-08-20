# standard imports
import unittest
import logging
import os
import datetime
import time
import base64

# external imports
from http_token_auth import SessionStore
from http_token_auth.error import TokenExpiredError

# local imports
from usumbufu.filter.session import SessionFilter
from usumbufu.ext.http import HTTPAuthorization
from usumbufu.retrieve import Retriever

# testutil imports
from tests.base import TestBaseAuth

script_dir = os.path.realpath(os.path.dirname(__file__))

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

ip = '127.0.0.1'
realm = 'foorealm'
host = 'localhost'
origin = 'http://' + host + ':5555'


class TestSessionAuth(TestBaseAuth):

    def test_get_by_auth_token(self):
        session_store = SessionStore()
        session_filter = SessionFilter(session_store)
        k = os.urandom(32)
        session_filter.decode(ip, k)
        session = session_store.get(k)
        self.assertEqual(session.identity, k)

        session = session_store.get(session.auth)
        self.assertEqual(session.identity, k)


    def test_http_bearer(self):
        session_store = SessionStore()
        session_filter = SessionFilter(session_store)
        k = os.urandom(32)
        session_filter.decode(ip, k)
        r = session_store.get(k)
        kb = base64.b64encode(r.auth)
        auth_string = 'Bearer {}'.format(kb.decode('utf-8'))

        retriever = Retriever()
        retriever.add_decoder(session_filter)
        authentication = HTTPAuthorization(realm, retriever, ip, auth_string, origin=origin)
    
        o = authentication.check()
        logg.debug('o {}'.format(o))


    def test_http_bearer_expire_noauto(self):
        session_store = SessionStore(auth_expire_delta=0.000001)
        session_filter = SessionFilter(session_store, autorefresh=False)
        k = os.urandom(32)
        session_filter.decode(ip, k)

        time.sleep(0.000001)
        with self.assertRaises(TokenExpiredError):
            r = session_store.get(k)


    def test_http_bearer_expire_auto(self):
        session_store = SessionStore(auth_expire_delta=0.000001)
        session_filter = SessionFilter(session_store, autorefresh=True)
        k = os.urandom(32)

        session_filter.decode(ip, k)
        one = session_store.session[k].auth
        self.assertIsNotNone(one)

        time.sleep(0.000001)
        session_filter.decode(ip, k)
        two = session_store.session[k].auth
        self.assertIsNotNone(two)
        self.assertNotEqual(one, two)


if __name__ == '__main__':
    unittest.main()
