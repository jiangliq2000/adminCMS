from flask import Blueprint

rest = Blueprint('rest', __name__)

from . import memberapi, teacherapi, studentapi, administratorapi
