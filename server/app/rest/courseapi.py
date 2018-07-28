from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Course as CourseModel
from app.model import Lesson as LessonModel
from app.model import Courseteacher as CTeacherModel
import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)


#query all course
@rest.route('courses/', methods=['GET'])
#@jwt_required()
def get_courses():
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    name = request.args.get('name')
    if name:
        total, courses = CourseModel.SearchCourseByName(page, limit, name)
    else:
        total, courses = CourseModel.GetCourses(page, limit)
    # get relation lessons information
    for i in range(len(courses)):
        courses[i]['lessonInfo'] = []
        #query student according members[i]['id']
        lessons = LessonModel.GetLessonsByCourseid(courses[i]['id'])
        for lesson in lessons:
            # get lesson information
            courses[i]['lessonInfo'].append(lesson)
        courses[i]['teacherInfo'] = []
        teachers = CTeacherModel.GetTeacherByCourseid(courses[i]['id'])
        for th in teachers:
            courses[i]['teacherInfo'].append({'teacher_id':th['teacher_id'],'teacher_name':th['teacher_name'],'teacher_mobile':th['teacher_mobile']})
    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'courses':courses})



# query one course
@rest.route('courses/<name>', methods=['GET'])
#@jwt_required()
def get_onecourse(name):
    courses = []
    course = CourseModel.GetOneCourseByName(name)
    if courses:
        courses.append(course)
    return utils.jsonresp(jsonobj={'courses':courses})

# create one course
@rest.route('courses/', methods=['POST'])
#@jwt_required()
def create_course():
    data = request.get_json('content')
    errcode = CourseModel.CreateCourse(data)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# update one course
@rest.route('courses/<name>', methods=['PUT'])
#@jwt_required()
def update_course(name):
    data = request.get_json(force=True) 
    errcode = CourseModel.UpdateCourseByName(data)
    return utils.jsonresp(jsonobj={'errcode':errcode})



# delete one course
@rest.route('courses/<name>', methods=['DELETE'])
#@jwt_required()
def delete_course(name):
    errcode = CourseModel.DeleteCourseByname(name)
    return utils.jsonresp(jsonobj={'errcode':errcode})


# patch one course
@rest.route('courses/batch/<names>', methods=['DELETE'])
#@jwt_required()
def delete_courses(names):
    errcode = 0
    #nameList = names.split(',')
    for name in names.split(','):
        ret = CourseModel.DeleteCourseByname(name)
        if ret != 0:
            errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode})

