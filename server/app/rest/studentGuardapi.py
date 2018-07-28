from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Studentguarder as StdGuarderModel
from app.model import Member as MemModel
from app.model import Student as StdModel
import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)


#query all students
@rest.route('studentGuards/', methods=['GET'])
@jwt_required()
def get_studentGuards():
    """
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    name = request.args.get('name')
    if name:
        total, students = StdGuarderModel.SearchStudentByName(page, limit, name)
    else:
        total, students = StdGuarderModel.GetStudents(page, limit)
    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'students':students})
    """
    pass

# create one student
@rest.route('studentGuards/', methods=['POST'])
@jwt_required()
def create_studentguard():
    print('receive post reqeust')
    data = request.get_json('content')
    print(type(data))
    print(data);
    stdGuardDict = {}
    if 'relationship' in data:
        stdGuardDict['relationship'] = int(data['relationship'])
    if 'focus' in data:
        stdGuardDict['focus'] = int(data['focus'])
    
    # query memmobile to get id
    recMem = MemModel.SearchMemberByMobile(data['memmobile'])
    #print(recMem)
    if recMem:
        stdGuardDict['member_id'] = recMem['id']
    else:
        return utils.jsonresp(jsonobj={'errcode':400})

    if 'studentids' in data:
        for uid in data['studentids']:
            # query uid to get id   
            recStd = StdModel.SearchStudentByUid(uid)
            print(recStd)
            if recStd:
                stdGuardDict['student_id'] = recStd['id']
                print('studentguard')
                print(stdGuardDict)
                errcode = StdGuarderModel.CreateStudentguarder(stdGuardDict)
    else:
        errcode = 400
    return utils.jsonresp(jsonobj={'errcode':errcode})

# query according studentId
@rest.route('studentGuards/studentid/<uid>', methods=['GET'])
@jwt_required()
def get_BystudentId_guard(uid):
    """
    students = []
    student = StdGuarderModel.SearchStudentByUid(uid)
    if student:
        students.append(student)
    return utils.jsonresp(jsonobj={'students':students})
    """
    pass


# update one student
@rest.route('studentGuards/studentid/<uid>', methods=['PUT'])
@jwt_required()
def update_student_guard(uid):
    """
    data = request.get_json(force=True) 
    #dataDict = utils.str_to_dict(rm.get_dict())
    errcode = StdGuarderModel.UpdateStudentByUid(data)

    return utils.jsonresp(jsonobj={'errcode':errcode})
    """
    pass


# get all students according member_id
@rest.route('studentGuards/memberid/<memid>', methods=['GET'])
@jwt_required()
def getStdsByMemid(memid):
    stdInfos =[]
    students = StdGuarderModel.GetStdsByMemid(memid)

    for std in students:
        # get student information
        stdinfo = StdModel.GetStdInfoById(std['student_id'])
        
        stdInfos.append({'id':std['student_id'],'name':stdinfo['name'], 'urgent_mobile':stdinfo['urgent_mobile'], 'relationship':std['relationship']})

    return utils.jsonresp(jsonobj={'students':stdInfos})


# update studentGuards records according member id
@rest.route('studentGuards/memberid/<memid>', methods=['PUT'])
@jwt_required()
def updateStdGuardByMemid(memid):
    errcode = 0
    data = request.get_json(force=True) 
    print("updateStdGuardByMemid data is")
    print(data)
    print(type(memid))
    #dataDict = utils.str_to_dict(rm.get_dict())
    #errcode = StdGuarderModel.UpdateStudentByUid(data)
    # 1.delet all records for current member id
    nums = StdGuarderModel.DelStdGuardByMemidStdid(int(memid))
    print("delete nums is :%d"%nums)
    # 2.create all records for student id in data
    stdGuardDict = {}
    stdGuardDict['member_id'] = int(memid)

    for std in data['corStudents']:
        stdGuardDict['student_id'] = std['id']
        stdGuardDict['relationship'] = std['relationship']
        errcode = StdGuarderModel.CreateStudentguarder(stdGuardDict)


    return utils.jsonresp(jsonobj={'errcode':errcode})




# delete one student
@rest.route('studentGuards/<uid>', methods=['DELETE'])
@jwt_required()
def delete_student_guard(uid):
    """
    errcode = StdGuarderModel.DeleteStudentByUid(uid)
    return utils.jsonresp(jsonobj={'errcode':errcode})
    """
    pass

# patch one student
@rest.route('studentGuards/batch/<uids>', methods=['DELETE'])
@jwt_required()
def delete_students_guard(uids):
    """
    errcode = 0
    for uid in uids.split(','):
        ret = StdGuarderModel.DeleteStudentByUid(uid)
        if ret != 0:
            errcode = 1
    return utils.jsonresp(jsonobj={'errcode':errcode})
    """
    pass

