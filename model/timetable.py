from . import DB
from pymongo.collection import Collection
from pymongo.read_preferences import ReadPreference


class TimeTable(object):
    COL_NAME = 'timetable'
    p_col = Collection(DB, COL_NAME)
    class Field(object):
        _id = '_id'
        id  = 'id'
        alarm = 'alarm'
        day = 'day'
        hour = 'hour'
        minute = 'minute'
        month = 'month'
        star = 'star'
        text = 'text'
        title = 'title'
        year = 'year'
        userId = 'userId'
