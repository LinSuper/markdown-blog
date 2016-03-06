from . import DB
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class MaxOrder(object):
    COL_NAME = 'max_order'
    p_col = Collection(DB, COL_NAME)
    class Field(object):
        _id = '_id'
        userId = 'userId'
        order = 'order'
