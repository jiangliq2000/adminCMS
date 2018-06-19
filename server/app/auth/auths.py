#from . import auth
from flask_jwt import JWT, current_identity,jwt_required
from app.model import Administrator 
from app import utils
from flask import Response, request
from werkzeug.security import check_password_hash, generate_password_hash,safe_str_cmp
from datetime import datetime

class Auth():
    def error_handler(self, e):
        print(e)
        return "password is not correct", 400

    def authenticate(self, username, password):
        user = Administrator.GetRecordByUsername(username)
        if user is None:
            self.error_handler('cannot find user')
        else:
            if safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
            #if check_password_hash(user.password, password):
                #update last_login_time and last_login_ip to database 
                user.lastlogintime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user.lastloginip = request.remote_addr
                user.save()
                return user
            else:
                self.error_handler('password is not correct')

    def identity(self, payload):
        userid = payload['identity']
        return Administrator.IsExistId(userid)



"""
# 身份认证
def authenticate(username, password):
    try:
        user = User.get(User.username == username)
        password_hash = user.password
        # if safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        if check_password_hash(password_hash, password):
            return user
    except:
        pass


# 返回身份信息
def identity(payload):
    user_id = payload['identity']
    user = User.get(User.id == user_id, User.status == True)
    return {'username': user.username, 'fullname': user.fullname, 'email': user.email, 'phone': user.phone}


# jwt = JWT(rest, authenticate, identity)

# 获取token
# POST /api/auth  {"username":"yourname","password":"yourpwd"}

# 获取用户信息
@auth.route('/identity')
@jwt_required()
def users_current():
    return Response(str(current_identity).replace("'", '"'), mimetype='application/json', status=200)

"""