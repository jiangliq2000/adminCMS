from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Student as StudentModel
import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)


#query all students
@rest.route('students/', methods=['GET'])
@jwt_required()
def get_students():
    print("recevie get all students requests")
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    name = request.args.get('name')
    if name:
        total, students = StudentModel.SearchStudentByName(page, limit, name)
    else:
        total, students = StudentModel.GetStudents(page, limit)
    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'students':students})


# query one student
@rest.route('students/<uid>', methods=['GET'])
@jwt_required()
def get_student(uid):
    students = []
    student = StudentModel.SearchStudentByUid(uid)
    if student:
        students.append(student)
    return utils.jsonresp(jsonobj={'students':students})

# query one or multi student
@rest.route('students/stdinfo/<sname>', methods=['GET'])
@jwt_required()
def GetStudentsInfoByName(sname):
    stdInfos = StudentModel.GetStudentsInfoByName(sname)
    return utils.jsonresp(jsonobj={'stdinfos':stdInfos})


# query one student info by ID
@rest.route('students/stdinfo/id/<sid>', methods=['GET'])
@jwt_required()
def GetStudentsInfoById(sid):
    stdInfos = StudentModel.GetStdInfoById(sid)
    return utils.jsonresp(jsonobj={'stdinfos':stdInfos})


# create one student
@rest.route('students/', methods=['POST'])
@jwt_required()
def create_student():
    print('receive post reqeust')
    data = request.get_json('content')
    errcode = StudentModel.CreateStudent(data)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# update one student
@rest.route('students/<uid>', methods=['PUT'])
@jwt_required()
def update_student(uid):
    data = request.get_json(force=True) 
    #dataDict = utils.str_to_dict(rm.get_dict())
    errcode = StudentModel.UpdateStudentByUid(data)

    return utils.jsonresp(jsonobj={'errcode':errcode})



# delete one student
@rest.route('students/<uid>', methods=['DELETE'])
@jwt_required()
def delete_student(uid):
    errcode = StudentModel.DeleteStudentByUid(uid)

    return utils.jsonresp(jsonobj={'errcode':errcode})


# patch one student
@rest.route('students/batch/<uids>', methods=['DELETE'])
@jwt_required()
def delete_students(uids):
    errcode = 0
    for uid in uids.split(','):
        ret = StudentModel.DeleteStudentByUid(uid)
        if ret != 0:
            errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode})

