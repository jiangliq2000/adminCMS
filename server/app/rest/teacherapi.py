from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Teacher as TeacherModel
import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)

# import faker data
#from app.mocks import teacher as fakerTeacher


#query all teachers
@rest.route('teachers/', methods=['GET'])
@jwt_required()
def get_teachers():
    print("recevie get all teachers requests")
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    name = request.args.get('name')
    if name:
        total, teachers = TeacherModel.SearchTeacherByName(page, limit, name)
    else:
        total, teachers = TeacherModel.GetTeachers(page, limit)
    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'teachers':teachers})


# query one teacher
@rest.route('teachers/<mobile>', methods=['GET'])
@jwt_required()
def get_teacher(mobile):
    teachers = []
    teacher = TeacherModel.SearchTeacherByMobile(mobile)
    if teacher:
        teachers.append(teacher)
    return utils.jsonresp(jsonobj={'teachers':teachers})

# create one teacher
@rest.route('teachers/', methods=['POST'])
@jwt_required()
def create_teacher():
    print('receive post reqeust')
    data = request.get_json('content')
    errcode = TeacherModel.CreateTeacher(data)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# update one teacher
@rest.route('teachers/<nickname>', methods=['PUT'])
@jwt_required()
def update_teacher(nickname):
    print(datetime.datetime.now())
    print('request put request')
    print(datetime.datetime.now())
    data = request.get_json(force=True) 
    print(datetime.datetime.now())
    print(data)
    #dataDict = utils.str_to_dict(rm.get_dict())
    errcode = TeacherModel.UpdateTeacherById(data)

    return utils.jsonresp(jsonobj={'errcode':errcode})



# delete one teacher
@rest.route('teachers/<nickname>', methods=['DELETE'])
@jwt_required()
def delete_teacher(nickname):
    errcode = TeacherModel.DeleteTeacherByNickname(nickname)

    return utils.jsonresp(jsonobj={'errcode':errcode})


# patch one teacher
@rest.route('teachers/batch/<nicknames>', methods=['DELETE'])
@jwt_required()
def delete_teachers(nicknames):
    errcode = 0
    #nameList = nicknames.split(',')
    for nickname in nicknames.split(','):
        ret = TeacherModel.DeleteTeacherByNickname(nickname)
        if ret != 0:
            errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode})

