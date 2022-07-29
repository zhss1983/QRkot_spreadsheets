import os
from pathlib import Path

class LoadSecrets():

    def __init__(self, secret_dir: str):
        self.secret_dir = Path(secret_dir).resolve()

    def __getattr__(self, name):
        attr = self.__dict__.get(name, None)
        if attr is not None:
            return attr
        filename = self.secret_dir / name
        if os.path.exists(filename):
            with open(filename, 'r') as secret:
                value = secret.read().strip(' \n\t\r')
                self.__dict__[name] = value
                return value
        raise AttributeError
