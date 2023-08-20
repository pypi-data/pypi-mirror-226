# standard imports
import logging

# external imports
from http_token_auth import SessionStore
from http_token_auth.error import ExpiredError
#from http_token_auth.error import TokenExpiredError

# local imports
from usumbufu.filter import Filter

logg = logging.getLogger(__name__)


class SessionFilter(Filter):

    default_name = 'session filter'

    def __init__(self, session_store, name=None, autorefresh=True):
        super(SessionFilter, self).__init__(name=name)
        self.session_store = session_store
        self.autorefresh = autorefresh


    def decode(self, requested_ip, v, signature=None, identity=None):
        session = None
        logg.debug('doing session')
        for k in self.session_store.session.keys():
            logg.warning('session k {}'.format(k))
        for k in self.session_store.session_reverse.keys():
            logg.warning('reverse k {}'.format(k))

        if identity == None:
            identity = v
        try:
            session = self.session_store.get(identity)
            return (session.identity, signature, session.identity)
        except ExpiredError as e:
            # a hack to enable use of session backend also when there is no separate auth (in which case refresh token is not known)
            if not self.autorefresh:
                raise e
            try:
                session = self.session_store.get_session(identity)
            except KeyError:
                session = self.session_store.check(v)
            auth_token = self.session_store.renew(session.identity, self.session_store.get_refresh(session.identity))
            session = self.session_store.check(auth_token)
            return (session.identity, signature, session.identity)
        except KeyError as e:
            pass


        if session == None:
            try:
                self.session_store.new(identity)
            except AttributeError:
                return None
            return (identity, signature, identity)

        return None 
