# standard imports
import logging
import uuid
import datetime

# local imports
from usumbufu.error import ChallengeError
from usumbufu.filter.util import source_hash

logg = logging.getLogger(__name__)

DEFAULT_CHALLENGE_EXPIRE = 10

class Challenge:

    def __init__(self, ip, expire=DEFAULT_CHALLENGE_EXPIRE):
        self.ip = ip
        uu = uuid.uuid4()
        self.value = uu.bytes
        self.expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire)


    def __str__(self):
        return 'challenge: ip {} challenge {} expire {} filter count {}'.format(
            self.ip,
            self.challenge,
            self.challenge_expire,
            self.filter,
            )


class Challenger:
    """Minimal convenience object representing an authentication challenge.

    :param ip: IP address of client
    :type p: str
    :param filters: List of filter methods to be executed on a challenge when apply_filters is called.
    :type filters: function, taking a single byte-string argument, returning a byte-string.
    """
    def __init__(self):
        self.challenges = {}
        

    def request(self, ip):
        """Creates a new challenge.

        :return: Challenge value
        :rtype: bytes
        """
        challenge = Challenge(ip)
        k = source_hash(ip, challenge.value)
        self.challenges[k] = challenge
        logg.debug('challenge {} ip {} stored under key {}'.format(challenge.value.hex(), ip, k.hex()))
        return (challenge.value, challenge.expires,)


    def clear(self, ip, challenge_value):
        k = source_hash(ip, challenge_value)
        del(self.challenges[k])


    def get(self, ip, v):
        k = source_hash(ip, v)
        challenge = self.challenges.get(k)
        if challenge == None:
            raise ChallengeError('challenge {} not found for ip {}'.format(v, ip))
        if challenge.ip != ip:
            raise ChallengeError('ip check mismatch: requester ip {} != challenged ip {}'.format(ip, challenge.ip))
        if challenge.expires <= datetime.datetime.utcnow():
            self.clear(ip, v)
            raise ChallengeError('challenge {} expired'.format(challenge.expires))
        return challenge.value
