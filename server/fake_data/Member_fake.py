# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn
import datetime
import json

from mocks import member as memberMock
from playhouse.shortcuts import model_to_dict, dict_to_model

db = MySQLDatabase(host='sh-cdb-j421jq38.sql.tencentcdb.com', port=63471,  user='root', passwd='Joyfulkid123', database='joy_userdb', charset='utf8')

class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


# 会员管理
class Member(BaseModel):
    class Meta:
        db_table = 'member' 

    nickname = CharField(unique=True) # 会员id
    name = CharField()           # 会员姓名
    sex  = IntegerField()        # 性别
    address = CharField()
    province = CharField()
    city = CharField()
    country = CharField()
    wxunionid = CharField()
    memtype = IntegerField()
    mobile = CharField()
    email = CharField()
    birthday = DateField()
    education = CharField()
    industry = CharField()
    background = CharField()
    changetime = DateTimeField()
    createtime = DateTimeField()
    emailVerified = IntegerField()
    lastloginip = CharField()
    lastdevice = CharField()
    lastlogintime = DateTimeField()
    balance = DecimalField(max_digits=10, decimal_places=2)
    school_id = IntegerField()
    inviter_id = IntegerField()
    status = IntegerField()


# 建表
def create_table():
    print("will create a table")
    db.connect()
    db.create_tables([Member])
    print("create table done ...")

def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


# insert member 
def InsertMember():
    m_fake = memberMock.Member()
    m_fake_dict = dict((name, getattr(m_fake,name)) for name in dir(m_fake) if not name.startswith('__') and not callable(getattr(m_fake,name)))
    m = dict_to_model(Member, m_fake_dict)
    m.save()

def GetMembers(page_num, item_per_page):
    count = Member.select().count()
    print("total record nums: %d" %count)
    memItems = []
    
    for mem in Member.select().order_by(Member.id).paginate(page_num, item_per_page):
        memItems.append(mem)
        print("%d"%mem.id + "  " + mem.name)
    print(memItems)   

def SearchMemberById(memberid):
    mem = Member.get_or_none(Member.memberid == memberid)
    return mem

def SearchMemberByMobile(mobile):
    mem = Member.get_or_none(Member.mobile == mobile)
    return mem


def SearchMemberByName(name):
    memList = []
    for mem in Member.select().where(Member.name == name):
        memList.append(mem)

    return memList

def UpdateMemberById(memberid):
    m_fake = memberMock.Member()
    m_fake_dict = dict((name, getattr(m_fake,name)) for name in dir(m_fake) if not name.startswith('__') and not callable(getattr(m_fake, name)))
    print(m_fake_dict)
    m_fake_dict['memberid'] = memberid
    m = Member.update(**m_fake_dict).where(Member.memberid==memberid).execute()
    print("m is ")
    print(m)
    if m == 1:
        print("update successfully")
    else:
        print("update failure")



def DeleteMemberById(memberid):
    m = Member.update(status='invalid').where(Member.memberid==memberid).execute()
    print("m is ")
    print(m)
    if m == 1:
        print("delete successfully")
    else:
        print("delete failure")



if __name__ == '__main__':
    
    create_table()
    for i in range(25):
        InsertMember()
    """
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
    """

    # delete a member
    #DeleteMemberById(45481440)


    # update a memeber  
    #UpdateMemberById(92596066)
    #GetMembers(1,5)
