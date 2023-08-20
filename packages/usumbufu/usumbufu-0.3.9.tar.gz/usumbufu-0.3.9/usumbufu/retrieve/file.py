# standard imports
import os

# local imports
from .base import (
        Fetcher,
        Retriever,
        )


class FileFetcher(Fetcher):

    default_name = 'file fetcher'

    def __init__(self, directory, name=None):
        super(FileFetcher, self).__init__(name=name)
        self.directory = directory


    def get(self, auth_string):
        for filename in os.listdir(self.directory):
            if filename == auth_string:
                f = open(os.path.join(self.directory, filename), 'rb')
                r = f.read()
                f.close()
                return r
        return None
