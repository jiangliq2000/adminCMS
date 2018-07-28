from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from app.model import Member as MemberModel
from app.model import Studentguarder as StdGuarderModel
from app.model import Student as StdModel
from app.model import Teacher as TeacherModel
import logging, datetime
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)

# import faker data
#from app.mocks import member as fakerMember


#query all members
@rest.route('members/', methods=['GET'])
@jwt_required()
def get_members():
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    name = request.args.get('name')
    if name:
        total, members = MemberModel.SearchMemberByName(page, limit, name)
    else:
        total, members = MemberModel.GetMembers(page, limit)  
    # get relation student information
    for i in range(len(members)):
        members[i]['studentInfo'] = []
        #query student according members[i]['id']
        stdids = StdGuarderModel.GetStdIdByMemid(members[i]['id'])
        if stdids:
            for sid in stdids:
                # get student information
                stdinfo = StdModel.GetStdInfoById(sid)
                members[i]['studentInfo'].append(stdinfo)
    return utils.jsonresp(jsonobj={'total':total, 'limit':limit, 'members':members})


# query one member
@rest.route('members/<mobile>', methods=['GET'])
@jwt_required()
def get_member(mobile):
    members = []
    member = MemberModel.SearchMemberByMobile(mobile)
    if member:
        members.append(member)
    return utils.jsonresp(jsonobj={'members':members})

# create one member
@rest.route('members/', methods=['POST'])
@jwt_required()
def create_member():
    print('receive post reqeust')
    data = request.get_json('content')
    errcode = MemberModel.CreateMember(data)
    return utils.jsonresp(jsonobj={'errcode':errcode})

# update one member
@rest.route('members/<nickname>', methods=['PUT'])
@jwt_required()
def update_member(nickname):
    data = request.get_json(force=True) 
    #dataDict = utils.str_to_dict(rm.get_dict())
    errcode = MemberModel.UpdateMemberById(data)

    return utils.jsonresp(jsonobj={'errcode':errcode})



# delete one member
@rest.route('members/<nickname>', methods=['DELETE'])
@jwt_required()
def delete_member(nickname):
    errcode = MemberModel.DeleteMemberByNickname(nickname)

    return utils.jsonresp(jsonobj={'errcode':errcode})


# patch one member
@rest.route('members/batch/<nicknames>', methods=['DELETE'])
@jwt_required()
def delete_members(nicknames):
    errcode = 0
    #nameList = nicknames.split(',')
    for nickname in nicknames.split(','):
        ret = MemberModel.DeleteMemberByNickname(nickname)
        if ret != 0:
            errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode})

