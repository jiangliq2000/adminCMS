from flask_jwt import jwt_required
from flask import request
from . import rest
from app import utils
from werkzeug.security import safe_str_cmp
from app.model import Administrator as AdmModel
import logging
from logging.config import fileConfig
fileConfig('conf/log-app.conf')
logger = logging.getLogger(__name__)

# import faker data
#from app.mocks import teacher as fakerTeacher


# update one teacher
@rest.route('users/password', methods=['PUT'])
@jwt_required()
def update_password():
    
    msgList = ['修改密码成功', '原密码错误，验证失败', '新旧密码一致，无须修改', '该用户不存在']
    data = request.get_json(force=True) 

    # check if the old password is correct
    user = AdmModel.GetRecordByUsername(data['username'])
    if user is None:
        errcode = 3
    else:
        if safe_str_cmp(data['oldpwd'].encode('utf-8'), user.password.encode('utf-8')):
            if safe_str_cmp(data['newpwd'].encode('utf-8'), user.password.encode('utf-8')):
                errcode = 2
            else:
                # update new password to database
                AdmModel.UpdateRecrodByUsername({'username':user.username, 'password':data['newpwd']})
                errcode = 0
        else:
            errcode = 1

    return utils.jsonresp(jsonobj={'errcode':errcode, 'errmsg':msgList[errcode]})


