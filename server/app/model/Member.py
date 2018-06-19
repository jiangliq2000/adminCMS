# -*- coding: utf-8 -*-
from app import utils
from app.model import Base
from app.model.Base import STATUS_INVALID, STATUS_VALID
from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn

from playhouse.shortcuts import model_to_dict, dict_to_model

from datetime import datetime



# 会员管理
class Member(Base.BaseModel):
    class Meta:
        db_table = 'member' 

    nickname = CharField(unique=True) # 会员id
    name = CharField()           # 会员姓名
    sex  = IntegerField()        # 性别
    #address = CharField()
    province = CharField(default='上海')
    city = CharField(default='上海')
    country = CharField(default='中国')
    wxunionid = CharField(default='0000')
    memtype = IntegerField()
    mobile = CharField()
    email = CharField()
    birthday = DateField(default='1970-01-01')
    education = CharField()
    industry = CharField()
    background = CharField()
    changetime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    emailVerified = IntegerField(default=0)
    lastloginip = CharField(default='null')
    lastdevice = CharField(default='null')
    lastlogintime = DateTimeField(default='1970-01-01 00:00:00')
    balance = DecimalField(max_digits=10, decimal_places=2)
    school_id = IntegerField()
    inviter_id = IntegerField()
    status = IntegerField(default=STATUS_VALID)


def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


def Time2Str(objDict):
    # strftime("%Y-%m-%d %H:%M:%S")
    for k, v in objDict.items():
        if isinstance(v, datetime.date):
            objDict[k] = v.strftime("%Y-%m-%d")
        if isinstance(v, datetime):
            objDict[k] = v.strftime("%Y-%m-%d %H:%M:%S")


# insert member 
def InsertMember():
    m_fake = memberMock.Member()
    m_fake_dict = dict((name, getattr(m_fake,name)) for name in dir(m_fake) if not name.startswith('__') and not callable(getattr(m_fake,name)))
    m = dict_to_model(Member, m_fake_dict)
    m.save()

def GetMembers(page_num, item_per_page):
    count = Member.select().where(Member.status == STATUS_VALID).count()
    members = []
    print("total record nums: %d" %count)
    #memList = [model_to_dict(mem) for mem in Member.select().order_by(Member.id).paginate(page_num, item_per_page)]
    for mem in Member.select().where(Member.status == STATUS_VALID).order_by(Member.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        members.append(m)

    return count, members


def SearchMemberById(nickname):
    mem = Member.get_or_none(Member.nickname == nickname, Member.status == STATUS_VALID)
    m = model_to_dict(mem)
    m = utils.Time2Str(m)
    m = utils.Decimal2Str(m)
    return m

def SearchMemberByMobile(mobile):
    m = Member.get_or_none(Member.mobile == mobile, Member.status == STATUS_VALID)
    if m:
        m = model_to_dict(m)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
    return m


def SearchMemberByName(page_num, item_per_page,name):
    count = Member.select().where(Member.name == name, Member.status == STATUS_VALID).count()
    members = []
    #memList = [model_to_dict(mem) for mem in Member.select().order_by(Member.id).paginate(page_num, item_per_page)]
    for mem in Member.select().where(Member.name == name, Member.status == STATUS_VALID).order_by(Member.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        members.append(m)

    return count, members

# create member 
def CreateMember(mDict):
    errcode = 1
    print("will create a new record")
    print(mDict)
    m = dict_to_model(Member, mDict)
    m.save()
    mem = Member.get_or_none(Member.nickname == mDict['nickname'], Member.status == STATUS_VALID)
    if mem:
        errcode = 0
    return errcode

def UpdateMemberById(mDict):
    errcode = 1
    m = Member.update(**mDict).where(Member.nickname==mDict['nickname']).execute()
    if m == 1:
        errcode = 0
    return errcode

def DeleteMemberByNickname(nickname,status=STATUS_INVALID):
    # 0 mean delete successfully
    errcode = 1
    m = Member.update(status=status).where(Member.nickname==nickname).execute()
    if m == 1:
        errcode = 0
    return errcode



if __name__ == '__main__':
    pass
    """
    create_table()
    for i in range(15):
        InsertMember()
    #InsertTeacher()
    #InsertUser()

    #for i in range(1,4):
    #    GetMembers(i, 5)
     
    # query member by member id
    mem = SearchMemberById(901527124)
    if mem:
        #print(mem)
        print('%d'%mem.id + "  " + mem.name)
    else:
        print("cannot find this member")


    # query member by memmber name, there may exit many records
    memList = SearchMemberByName('孙宇')
    if memList:
        for mem in memList:
            print("id: %d"%mem.id + "  memberid:%d"%mem.memberid + "  name:" + mem.name)
    else:
        print("cannot find any records")

    # delete a member
    #DeleteMemberById(45481440)


    # update a memeber  
    #UpdateMemberById(92596066)
    count, memItems = GetMembers(1, 5) 
    print("total is : %d"%count)
    print(memItems)   
    """
