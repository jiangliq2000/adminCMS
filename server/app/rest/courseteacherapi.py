from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Courseteacher as CTeacherModel

import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)



# update courseteacher 
@rest.route('courseteachers/<cid>', methods=['PUT'])
#@jwt_required()
def update_courseteachers(cid):
    data = request.get_json(force=True) 
    courseid = int(cid)
    # step1 delete all records for course_id = courseid 
    CTeacherModel.DeleteByCourseid(courseid)

    # store all records for courseid 
    for ct in data['corTeachers']:
    	ctdict = {'course_id':courseid, 'teacher_id':int(ct['teacher_id']),'teacher_name':ct['teacher_name'],'teacher_mobile':ct['teacher_mobile']}
    	errcode = CTeacherModel.CreateCourseteacher(ctdict)

    return utils.jsonresp(jsonobj={'errcode':errcode})

