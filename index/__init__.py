# -*- coding: utf-8 -*-
from flask import Blueprint, request


index = Blueprint('/index', __name__)


import user
import editor
import share
import blog
import mark_zone
import article