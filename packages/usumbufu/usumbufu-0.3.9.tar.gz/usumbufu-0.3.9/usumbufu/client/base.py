# standard imports
import copy
import urllib.request
from http.client import HTTPResponse
import os
from email.utils import unquote
import datetime
import logging
import re
import hashlib
import base64

# local imports
from usumbufu.error import AuthenticationError

logg = logging.getLogger(__name__)


def split_auth_header(v):
    subsections = v.split(',')
    logg.debug('subs {}'.format(subsections))
    parts = {}
    for s in subsections:
        (k, v) = s.split('=', maxsplit=1)
        parts[k] = unquote(v)
    return parts 


def split_challenge_header(v, strict=True):
    o = split_auth_header(v)
    if o.get('challenge') == None:
        raise ValueError('challenge missing')
    elif strict:
        if o.get('max-age') == None or o.get('realm') == None:
            raise ValueError('strict parse fail') 
    return o


def challenge_nonce():
    return os.urandom(32)


def request_to_endpoint(rq):
    s = rq.full_url
    url = urllib.parse.urlsplit(s)
    return url.geturl()


class BaseTokenStore:

    def __init__(self, path=None):
        self.tokens = {}
        self.session_dates = {}
        self.path = path


    def __save(self, k, v):
        if self.path != None:
            h = hashlib.sha1()
            h.update(k.encode('utf-8'))
            z = h.digest()
            fn = os.path.join(self.path, z.hex())
            f = open(fn, 'wb')
            f.write(v)
            f.close()
            logg.debug('token saved to {}'.format(fn))


    def __load(self, k):
        if self.path != None:
            h = hashlib.sha1()
            h.update(k.encode('utf-8'))
            z = h.digest()
            fn = os.path.join(self.path, z.hex())
            try:
                f = open(fn, 'rb')
            except FileNotFoundError:
                return None
            v = f.read()
            f.close()
            logg.debug('token read from {}'.format(fn))
            return v


    def __remove(self, k):
        if self.path != None:
            h = hashlib.sha1()
            h.update(k.encode('utf-8'))
            z = h.digest()
            fn = os.path.join(self.path, z.hex())
            os.unlink(fn)
            logg.debug('removed token {} from'.format(fn))


    def get(self, k):
        r = self.tokens.get(k)
        if r == None:
            r = self.__load(k)
        return r


    def get_by_request(self, rq):
        k = request_to_endpoint(rq)
        return self.get(k)
   

    def put(self, k, v):
        self.tokens[k] = v
        self.session_dates[k] = datetime.datetime.utcnow()
        self.__save(k, v)


    def put_by_request(self, rq, token):
        k = request_to_endpoint(rq)
        self.put(k, token)
  

    def remove(self, k):
        try:
            del self.tokens[k]
        except KeyError:
            pass
        self.__remove(k)


    def remove_by_request(self, rq):
        k = request_to_endpoint(rq)
        self.remove(k)


re_auth = r'^(\w+) (.+)$'
class ClientSession(urllib.request.HTTPSHandler):

    def __init__(self, origin, token_store=None, ssl_context=None):
        super(ClientSession, self).__init__(context=ssl_context)
        self.origin = origin
        self.token_store = token_store
        self.__handlers = [self]
        self.__handler_crsr = 0


    def add_subhandler(self, handler):
        #hndlr = self.__handlers.append(handler)
        hndlr = self.__handlers.insert(-1, handler)
        logg.info('registered handler {} in position {}'.format(handler, len(self.__handlers)))


    def get_handler(self):
        r = None
        try:
            r = self.__handlers[self.__handler_crsr]
        except IndexError:
            self.__handler_crsr = 0
        return r


    def set_token(self, request, token):
        logg.debug('setting auth token {}'.format(token))
        self.token_store.put_by_request(request, token)


    def http_request(self, request):
        hndlr = self.get_handler()
        if hndlr == None:
            raise AuthenticationError()
        return hndlr.process_auth_request(request)


    def https_request(self, request):
        return self.http_request(request)


    def http_error_400(self, request, response, code, msg, hdrs):
        return response


    def http_error_404(self, request, response, code, msg, hdrs):
        return response


    def http_error_401(self, request, response, code, msg, hdrs):
        h = hdrs.get('WWW-Authenticate')
        if h == None:
            raise urllib.error.HTTPError(request.full_url, 403, 'No authenticate method found', hdrs, None)

        m = re.match(re_auth, h)
        method = m.group(1)
        details = m.group(2)
        logg.debug('auth method {} requested with: {}'.format(method, details))
        
        hndlr = self.get_handler()
        if hndlr == None:
            raise urllib.error.HTTPError(request.full_url, code, 'No valid handlers for authentication challenge {}'.format(h), hdrs, None)
        logg.debug('handling 401 with handler {}'.format(hndlr))
        self.__handler_crsr += 1

        try:
            auth_response = hndlr.process_auth_challenge(details, method=method)
        except NotImplementedError:
            return self.http_error_401(request, response, code, msg, hdrs)

        request.headers['Authorization'] = '{} {}'.format(method, auth_response)
        opener = urllib.request.build_opener(self)
        try:
            response = opener.open(request)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                logg.error('authentication failed: {} {}'.format(e.code, e.msg))
            logg.error('unexpected status code from auth short-circuit: {}'.format(e))
        
        token_bsf = response.headers.get('Token')
        if token_bsf == None:
            logg.debug('missing token from headers; {}'.format(response.getheaders()))
            raise AuthenticationError('No token received from any authentication method')

        self.set_token(request, base64.b64decode(token_bsf))

        return response


    def http_error_403(self, request, response, code, msg, hdrs):
        self.token_store.remove_by_request(request)
        logg.debug('oh hno')
        return response


    def process_auth_challenge(self, header, encoding=None, method=None):
        raise NotImplementedError('override this class to create an auth challenge handler for authorization method {}'.format(method))


    def process_auth_request(self, request):
        return request


    def __str__(self):
        return 'usumbufu ' + str(self.__handlers[:len(self.__handlers)-1])
