# standard imports
import hashlib

# local imports
from ..auth import Auth


class OauthClientAuthorization(Auth):
    """Handles a Oauth client_id access code authentication request. It can be used to authenticate a client attempting to perform Oauth authorization.

    The value user to retrieve the authentication data is the sha256 value of the literal client_id string.
    """

    component_id = 'oauth_client_request'


    """Implements Auth.check
    """
    def check(self):
        auth_string_bytes = self.auth_string.encode('utf-8')
        h = hashlib.sha256()
        h.update(auth_string_bytes)
        auth_string = h.digest()
        auth_data = self.retriever(auth_string)
        if auth_data == None:
            return None
        return (self.component_id, auth_string, auth_data)


    """Implements Auth.method
    """
    def method(self):
        return None
