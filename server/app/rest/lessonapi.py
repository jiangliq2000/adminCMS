from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Lesson as LessonModel
from app.model import Course as CourseModel
import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)


#query all lessons
@rest.route('lessons/', methods=['GET'])
#@jwt_required()
def get_lessons():
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    name = request.args.get('lessonname')
    if name:
        total, lessons = LessonModel.SearchLessonByName(page, limit, name)
    else:
        total, lessons = LessonModel.GetLessons(page, limit)
    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'lessons':lessons})


# query one lesson by lesson id
@rest.route('lessons/id/<lid>', methods=['GET'])
#@jwt_required()
def get_lessonById(lid):
    return utils.jsonresp(jsonobj={'lesson':LessonModel.GetLessonsBylessonid(lid)})

# query lessons by name
@rest.route('lessons/<name>', methods=['GET'])
#@jwt_required()
def get_lessonsByName(name):
    lessons = LessonModel.GetLessonsByName(name)
    for i in range(len(lessons)):
        cName = CourseModel.GetNameById(lessons[i]['course_id'])
        lessons[i]['coursename'] = cName
    return utils.jsonresp(jsonobj={'lessons':lessons})

# create one lesson
@rest.route('lessons/', methods=['POST'])
#@jwt_required()
def create_lesson():
    data = request.get_json('content')
    errcode = LessonModel.CreateLesson(data)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# update one lesson
@rest.route('lessons/<name>', methods=['PUT'])
#@jwt_required()
def update_lesson(name):
    data = request.get_json(force=True) 
    errcode = LessonModel.UpdateLessonByName(data)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# update courseid by lessnon id
@rest.route('lessons/courseid/<cid>', methods=['PUT'])
#@jwt_required()
def updateCidBylessonid(cid):
    data = request.get_json(force=True) 
    courseid = int(cid)
    # step1 reset courseid to 0 for current all lesson
    # courseid = 0 , it mean no correlation for this lesson
    for lesson in LessonModel.GetLessonsByCourseid(courseid):
        LessonModel.UpdateCidByLid(0, lesson['id']) 

    # step2 update courseid according to lessonid 
    for lid in data['corLessonids']:
        errcode = LessonModel.UpdateCidByLid(courseid,int(lid))
    return utils.jsonresp(jsonobj={'errcode':errcode})



# delete one lesson
@rest.route('lessons/<name>', methods=['DELETE'])
#@jwt_required()
def delete_lesson(name):
    errcode = LessonModel.DeleteLessonByname(name)
    return utils.jsonresp(jsonobj={'errcode':errcode})


# patch one lesson
@rest.route('lessons/batch/<names>', methods=['DELETE'])
#@jwt_required()
def delete_lessons(names):
    errcode = 0
    #nameList = names.split(',')
    for name in names.split(','):
        ret = LessonModel.DeleteLessonByname(name)
        if ret != 0:
            errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode})

