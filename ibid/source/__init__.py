from copy import copy

class IbidSourceFactory(object):

    supports = ()
    auth = ()
    permissions = ()

    def __new__(cls, *args):
        cls.type = cls.__module__.split('.')[2]

        for name, option in options.items():
            new = copy(option)
            default = getattr(cls, name)
            new.default = default
            setattr(cls, name, new)

        return super(IbidSourceFactory, cls).__new__(cls, *args)

    def __init__(self, name):
        self.name = name

    def setServiceParent(self, service):
        raise NotImplementedError

    def connect(self):
        return self.setServiceParent(None)

    def disconnect(self):
        raise NotImplementedError

    def url(self):
        return None

    def logging_name(self, identity):
        "Given an identity or connection, return a name suitable for logging"
        return identity

from ibid.config import Option

options = {
    'auth': Option('auth', 'Authentication methods to allow'),
    'permissions': Option('permissions', 'Permissions granted to users on this source')
}
# vi: set et sta sw=4 ts=4:
