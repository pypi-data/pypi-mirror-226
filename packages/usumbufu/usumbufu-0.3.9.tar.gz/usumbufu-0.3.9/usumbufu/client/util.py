# standard imports
import re


def get_auth_header_parts(h):
    m = re.match(r'^([a-zA-Z]+) (.+)$', h)
    if m == None:
        raise ValueError('invalid auth header {}'.format(h))
    method = m[1]
    return (method, get_header_parts(m[2]),)


def get_header_parts(h):
    hp = h.split(',')
    ap = {}
    for p in hp:
        m = re.match(r'^(.+)="(.+)"', p)
        ap[m[1]] = m[2]
    return ap
