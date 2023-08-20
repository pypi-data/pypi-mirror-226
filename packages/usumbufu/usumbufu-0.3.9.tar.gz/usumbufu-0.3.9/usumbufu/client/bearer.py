# standard imports
import logging
import base64

# local imports
from .base import ClientSession

logg = logging.getLogger(__name__)


class BearerClientSession:

    def __init__(self, origin, token_store=None):
        self.token_store = token_store


    def process_auth_request(self, request):
        if request.headers.get('Authorization') == None:
            token = self.token_store.get_by_request(request)
            if token != None:
                request.add_header('Authorization', 'Bearer {}'.format(base64.b64encode(token).decode('utf-8')))
            else:     
                logg.debug('no active auth token found for {}'.format(request.full_url))
        return request


    def process_auth_challenge(self, header, encoding=None, method=None):
        raise NotImplementedError()
         

    def __repr__(self):
        return 'bearer'

    def process_auth_challenge(self, header, encoding=None, method=None):
        raise NotImplementedError()
         

    def __str__(self):
        return 'bearer'

