class Filter:

    default_name = 'filter prototype'

    def __init__(self, name=None):
        self.name = name or self.default_name


    def decode(self, requester_ip, v, signature=None, identity=None):
        raise NotImplementedError


    def encode(self, requester_ip, v):
        raise NotImplementedError


    def __str__(self):
        return self.name
