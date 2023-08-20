# standard imports
import hashlib


def source_hash(ip, data):
    """Creates a unique index value for a combination of (client) ip and challenge data.

    :param ip: IP address in text format, translated to bytes
    :type ip: bytes
    :param data: The data represented by the index
    :type data: bytes
    :return: Preimage of ip and data
    :rtype: bytes
    """
    h = hashlib.sha256()
    h.update(ip.encode('utf-8'))
    h.update(data)
    k = h.digest()
    return k
