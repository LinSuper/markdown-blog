# -*- coding: utf-8 -*-
from config import (
    MONGO_PWD,
    MONGO_HOST,
    MONGO_USER,
    MONGO_DATABASE,
    IS_MONGO_AUTH
)
from pymongo import MongoClient


client = MongoClient(MONGO_HOST)
DB = client[MONGO_DATABASE]
if IS_MONGO_AUTH:
    DB.authenticate(MONGO_USER, MONGO_PWD)
