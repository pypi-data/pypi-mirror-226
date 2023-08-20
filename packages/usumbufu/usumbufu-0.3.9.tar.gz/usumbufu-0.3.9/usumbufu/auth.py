# standard import
import logging

# local imports
from usumbufu.error import AuthenticationError

logg = logging.getLogger(__name__)


class Auth:


    """Base class and interface for authentication backends
    :param component_id: the id of the component
    :type component_id str
    :param retriever: Retriever object to access authentication data
    :type retriever: function
    :param auth_string: Authentication string
    :type auth_string: str
    :param realm: Authentication realm, optional
    :type realm: str
    """
    def __init__(self, realm=None):
        self.component_id = None
        self.retriever = None
        self.auth_string = None
        self.realm = realm


    def update(self, retriever=None, auth_string=None, component_id=None):
        if retriever != None:
            self.retriever = retriever

        if auth_string != None:
            self.auth_string = auth_string

        if component_id != None:
            self.component_id = component_id


    """Interface method.

    In implementation it should execute the authentication lookup with the current state of data.

    :returns: None on failure, or tuple (authentication component id, authentication string, authentication data)
    :rtype: tuple or None
    """
    def check(self):
        return None


class AuthVector:
    """Holds a collection of authentication methods to be attempted. All members of the collection are expected to implement the usumbufu.Auth interface.

    All activated authenticators will be tried in order that they are added, and will return on the first method that succeeds.
    """
    def __init__(self):
        self.authenticators = {}
        self.authenticators_active = []


    """Implements AuthAdapter.register
    """
    def register(self, authenticator):
        self.authenticators[authenticator.component_id] = authenticator
        logg.debug(str(self.authenticators) + ' ' + authenticator.component_id)


    """Implements AuthAdapter.activate
    """
    def activate(self, component_id):
        self.authenticators_active.append(component_id)
        logg.debug(str(self.authenticators_active))

    """Implements AuthAdapter.check
    """
    def check(self):
        t = None
        for k in self.authenticators_active:
            logg.debug('k {}'.format(k))
            authenticator = self.authenticators[k]
            try:
                t = authenticator.check()
                if t:
                    logg.info('authentication success {} {}'.format(k, t))
                    return t
            except AuthenticationError as e:
                logg.debug('authentication failed: {}'.format(authenticator))
        return None
