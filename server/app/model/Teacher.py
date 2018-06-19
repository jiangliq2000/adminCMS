# -*- coding: utf-8 -*-
from app import utils
from app.model import Base
from app.model.Base import STATUS_INVALID, STATUS_VALID
from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn

from playhouse.shortcuts import model_to_dict, dict_to_model
#from playhouse.flask_utils import FlaskDB
from datetime import datetime


# 教师管理
class Teacher(Base.BaseModel):
    class Meta:
        db_table = 'teacher' 

    name = CharField()
    password = CharField()
    options = CharField()
    nickname = CharField()
    sex  = IntegerField() 
    province = CharField()
    city = CharField()
    country = CharField()
    mobile = CharField()
    email = CharField()
    #address = CharField()
    birthday = DateField(default='1970-01-01')
    education = CharField()
    school_id = IntegerField()
    image_url = CharField()
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = IntegerField(default=STATUS_VALID)


# insert teacher 
def InsertTeacher():
    m_fake = teacherMock.teacher()
    m_fake_dict = dict((name, getattr(m_fake,name)) for name in dir(m_fake) if not name.startswith('__') and not callable(getattr(m_fake,name)))
    m = dict_to_model(teacher, m_fake_dict)
    m.save()

def GetTeachers(page_num, item_per_page):
    count = Teacher.select().where(Teacher.status == STATUS_VALID).count()
    teachers = []
    print("total record nums: %d" %count)
    #memList = [model_to_dict(mem) for mem in Teacher.select().order_by(Teacher.id).paginate(page_num, item_per_page)]
    for mem in Teacher.select().where(Teacher.status == STATUS_VALID).order_by(Teacher.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        teachers.append(m)

    return count, teachers


def SearchTeacherById(nickname):
    mem = Teacher.get_or_none(Teacher.nickname == nickname, Teacher.status == STATUS_VALID)
    m = model_to_dict(mem)
    m = utils.Time2Str(m)
    m = utils.Decimal2Str(m)
    return m

def SearchTeacherByMobile(mobile):
    m = Teacher.get_or_none(Teacher.mobile == mobile, Teacher.status == STATUS_VALID)
    if m:
        m = model_to_dict(m)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
    return m


def SearchTeacherByName(page_num, item_per_page,name):
    count = Teacher.select().where(Teacher.name == name, Teacher.status == STATUS_VALID).count()
    teachers = []
    #memList = [model_to_dict(mem) for mem in Teacher.select().order_by(Teacher.id).paginate(page_num, item_per_page)]
    for mem in Teacher.select().where(Teacher.name == name, Teacher.status == STATUS_VALID).order_by(Teacher.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        teachers.append(m)

    return count, teachers

# create teacher 
def CreateTeacher(mDict):
    errcode = 1
    m = dict_to_model(Teacher, mDict)
    m.save()
    mem = Teacher.get_or_none(Teacher.nickname == mDict['nickname'], Teacher.status == STATUS_VALID)
    if mem:
        errcode = 0
    return errcode

def UpdateTeacherById(mDict):
    errcode = 1
    m = Teacher.update(**mDict).where(Teacher.nickname==mDict['nickname']).execute()
    if m == 1:
        errcode = 0
    return errcode

def DeleteTeacherByNickname(nickname,status=STATUS_INVALID):
    # 0 mean delete successfully
    errcode = 1
    m = Teacher.update(status=status).where(Teacher.nickname==nickname).execute()
    if m == 1:
        errcode = 0
    return errcode



if __name__ == '__main__':
    pass
    """
    create_table()
    for i in range(15):
        Insertteacher()
    #InsertTeacher()
    #InsertUser()

    #for i in range(1,4):
    #    Getteachers(i, 5)
     
    # query teacher by teacher id
    mem = SearchteacherById(901527124)
    if mem:
        #print(mem)
        print('%d'%mem.id + "  " + mem.name)
    else:
        print("cannot find this teacher")


    # query teacher by memmber name, there may exit many records
    memList = SearchteacherByName('孙宇')
    if memList:
        for mem in memList:
            print("id: %d"%mem.id + "  teacherid:%d"%mem.teacherid + "  name:" + mem.name)
    else:
        print("cannot find any records")

    # delete a teacher
    #DeleteteacherById(45481440)


    # update a memeber  
    #UpdateteacherById(92596066)
    count, memItems = Getteachers(1, 5) 
    print("total is : %d"%count)
    print(memItems)   
    """
