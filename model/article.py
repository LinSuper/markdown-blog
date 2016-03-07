from . import DB
from pymongo.collection import Collection



class Article(object):
    COL_NAME = 'article'
    p_col = Collection(DB, COL_NAME)
    class Field(object):
        _id = '_id'
        user_id = 'user_id'
        content = 'content'
        title = 'title'
        create_time = 'create_time'
        type = 'type'

    class TypeFiled(object):
        public = 0
        private = 1