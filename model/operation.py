from . import DB
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class Operation(object):
    COL_NAME = 'operation'
    p_col = Collection(DB, COL_NAME)
    class Field(object):
        _id = '_id'
        order = 'order'
        trye = 'type'
        op = 'op'
