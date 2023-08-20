# standard imports
import logging

# local imports
from usumbufu.auth import Auth


class QueryString(Auth):
    """Handles the authentication parameters used when "username" and "password" are query string parameters

    :param fetcher: Callback used to retrieve authentication data based on the authorization string digest
    :type fetcher: function
    :param auth_string: Username and password.
    :type auth_string: sstr
    """
    logger = logging.getLogger(__name__)


    def __init__(self, fetcher, auth_string, ips=[]):
        super(QueryString, self).__init__()
        self.component_id = 'querystring'
        self.auth_string= auth_string
        self.retriever = fetcher
        self.ips = ips
        if len(self.ips) == 0:
            logg.warning('no ips in querystring authenticator. ip check will be deactivated')


    def check(self):
        """Implements Auth.check
        """
        self.logger.debug('querystring check')
        if self.current_ip not in self.ips:
            self.logger.info('querystring ip {} not in whitelist'.format(self.current_ip))
            return None
        if self.auth_string == None:
            self.logger.debug('no authstring found')
            return None
        auth_data = self.retriever.load(self.current_ip, self.auth_string)
        if auth_data == None:
            return None
        return (self.component_id, self.auth_string, auth_data)
