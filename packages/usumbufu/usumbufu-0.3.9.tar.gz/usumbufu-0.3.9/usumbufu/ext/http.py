# standard imports
import logging
import base64
import hashlib
import re

# external imports
from http_hoba_auth import Hoba
from usumbufu.error import AuthenticationError

# local imports
from ..auth import Auth

logg = logging.getLogger()


class HTTPAuthorization(Auth):
    """Handles HTTP authorization methods.

    Currently implemented schemes are Basic, Bearer and HOBA. The scheme is determined by the auth string. 

    The digest value used to retrieve authentication data depends on the scheme:

    - Basic: sha256(user:pass), or sha256(user:pass, client_id) if client_id is supplied
    - HOBA: The public key of the client
    - Bearer: The token value

    :param fetcher: Callback used to retrieve authentication data based on the authorization string digest
    :type fetcher: function
    :param http_auth_string: The HTTP "Authorization" header value
    :type http_auth_string: str
    :param realm: Authentication realm
    :type realm: str
    :param client_id: Oauth client_id of entity performing authentication, optional
    :type client_id: str
    """
    re = r'^(\w+) (.+)?$'
    logger = logging.getLogger(__name__)

    def __init__(self, realm, retriever, ip, http_auth_string, client_id=None, origin=None):
        super(HTTPAuthorization, self).__init__(realm=realm)
        self.realm = realm
        self.origin = origin
        self.ip = ip
        method = None
        auth_value = None
        try:
            m = re.match(self.re, http_auth_string)
            method = m[1].lower()
            auth_value = m[2]
            logg.debug('processed auth string {}'.format(http_auth_string))
        except TypeError:
            pass

        auth_string = None
        if method == None:
            logg.debug('invalid auth string, this http authenticator will not be executing')
        elif method== 'bearer':
            (auth_string, retriever) = self.__handle_bearer(auth_value, retriever, client_id)
        elif method == 'basic':
            (auth_string, retriever) = self.__handle_basic(auth_value, retriever, client_id)
        elif method == 'hoba':
            (auth_string, retriever) = self.__handle_hoba(auth_value, retriever, client_id)
        else:
            logg.warning('unhandled authorization scheme {}'.format(method))
      
        self.update(auth_string=auth_string, retriever=retriever)

        
    # Handler code for "Authorization: Bearer" scheme
    def __handle_bearer(self, s, f, c):
        self.update(component_id='http-bearer')
        self.logger.debug('set component id {}'.format(self.component_id))
        try:
            auth_string = bytes.fromhex(s)
            return auth_string, f
        except:
            pass
        
        try:
            auth_string = base64.b64decode(s)
            return auth_string, f
        except:
            auth_string = s
        return (auth_string, f)


    # Handler code for "Authorization: HOBA" scheme
    def __handle_hoba(self, s, f, c):
        self.update(component_id='http-hoba')
        hoba = Hoba(self.origin, self.realm)
        hoba.parse(s)
        #self.logger.debug('user {} {} {}'.format(self.hoba_filter.challenge.hex(), self.origin, self.realm))
        #self.logger.debug('challenge raw {} {} {}'.format(s, f, c))
        #self.logger.debug('challenge parsed {} {} {} {}'.format(self.origin, self.ip, self.hoba_filter.challenge.hex(), self.hoba_filter.signature))
        #auth_string = f.validate(self.ip, self.hoba_filter.challenge, self.hoba_filter.signature)
        #auth_string = f.load(self.ip, s)
        #return (auth_string, f)
        return (str(hoba), f)


    # Handler code for "Authorization: Basic" scheme
    def __handle_basic(self, s, f, c):
        self.update(component_id='http-basic')
        self.logger.debug('set component id {}'.format(self.component_id))
        auth_string_bytes = base64.b64decode(s)
        h = hashlib.sha256()
        h.update(auth_string_bytes)
        if c != None:
            h.update(c.encode('utf-8'))
        auth_string = h.digest()
        (u, p) = auth_string_bytes.decode('utf-8').split(':')
        return (auth_string, f) 


    """Implements Auth.check
    """
    def check(self):
        self.logger.debug('{} check {}'.format(self.component_id, self.auth_string))
        if self.auth_string == None:
            self.logger.debug('no auth string for {}'.format(self.component_id))
            return None
        auth_data = None
        identity = None
        try:
            (auth_data, identity) = self.retriever.load(self.ip, self.auth_string)
        except Exception as e:
            logg.exception(e)
            logg.error('auth error received by retriever caller: {}'.format(e))
            raise AuthenticationError(str(e))
        if auth_data == None:
            raise AuthenticationError()
        return (self.component_id, self.auth_string, auth_data, identity)


def basic_auth_request_string(realm=None):
    s = 'Basic charset="UTF-8"'
    if realm != None:
        s += ', realm="{}"'.format(realm)
    return s
