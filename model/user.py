from . import DB
from flask.ext.login import UserMixin
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class User(UserMixin):
    COL_NAME = 'user'
    p_col = Collection(DB, COL_NAME)
    class Field(object):
        _id = '_id'
        username = 'username'
        password = 'password'
        phone = 'phone'
        token = 'token'
    def __init__(self, **kwargs):
        UserMixin.__init__(self)
        for k, v in kwargs.iteritems():
            self.__setattr__(k, v)
    def __getitem__(self, name):
        return self.__getattribute__(name)
    def get_id(self):
        return self._id
    def get_auth_token(self):
        return self.token
