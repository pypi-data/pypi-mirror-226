# standard import
import logging
import hashlib
from urllib.parse import parse_qs
import re
import time
import base64

# local imports
from usumbufu.ext.ssl import SSLClient
from usumbufu.ext.http import HTTPAuthorization
from usumbufu.ext.querystring import QueryString
from usumbufu.error import AuthenticationError
from usumbufu.auth import AuthVector

logg = logging.getLogger(__name__)


class UWSGIAdapter(AuthVector):
    pass


class UWSGISSLClient(SSLClient):
    """Adapts input and output between UWSGI and the SSLClient authenticator.

    :param fetcher: Callback used to retrieve authentication data based on the authorization string digest
    :type fetcher: function
    :param env: UWSGI environment variables
    :type env: dict
    """
    def __init__(self, fetcher, env):
        b = ''
        try:
             b = env['HTTPS_CLIENT_CERTIFICATE']
        except KeyError as e:
            self.logger.debug('no ssl client certificate')
        super(UWSGISSLClient, self).__init__(fetcher, env)
        # hack!! https://github.com/unbit/uwsgi/issues/1558
        self.auth_string = b.encode('ISO-8859-1')


    """Overrides SSLClient.check
    """
    def check(self):
        t = None
        try:
            t = super(UWSGISSLClient, self).check()
        except ValueError as e:
            self.logger.warning('Bogus client certificate data')

        return t


class UWSGIQueryString(QueryString):
    """Adapts input and output between UWSGI and the QueryString authenticator.

    :param fetcher: Callback used to retrieve authentication data based on the authorization string digest
    :type fetcher: function
    :param env: UWSGI environment variables
    :type env: dict
    """
    def __init__(self, fetcher, env, ips=[]):
        self.current_ip = env['REMOTE_ADDR']
        self.ips = ips
        q = parse_qs(env['QUERY_STRING'])
        auth_string = None
        try:
            auth_string = '{}:{}'.format(q['username'][0], q['password'][0])
            h = hashlib.sha256()
            h.update(auth_string.encode('utf-8'))
            auth_string = h.digest()
        except KeyError:
            self.logger.debug('no querystring auth data found')
        self.logger.debug('authstring {}'.format(auth_string))
        super(UWSGIQueryString, self).__init__(fetcher, auth_string, ips)


class UWSGIHTTPAuthorization(HTTPAuthorization):
    """Adapts input and output between UWSGI and the HTTPAuthorization authenticators.
    
    :param fetcher: Callback used to retrieve authentication data based on the authorization string digest
    :type fetcher: function
    :param env: UWSGI environment variables
    :type env: dict
    :param realm: Authentication realm
    :type realm: str
    :param client_id: Oauth client_id of entity performing authentication, optional
    :type client_id: str
    """
    def __init__(self, fetcher, env, realm, client_id=None, origin=None):
        auth_header = None
        ip = None
        try:
            auth_header = env['HTTP_AUTHORIZATION']
            ip = env['REMOTE_ADDR']
        except KeyError as e:
            self.logger.debug('invalid headers found, cannot perform HTTP auth {}'.format(e))
        super(UWSGIHTTPAuthorization, self).__init__(realm, fetcher, ip, auth_header, client_id=client_id, origin=origin)

