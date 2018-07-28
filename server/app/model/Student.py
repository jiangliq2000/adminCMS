# -*- coding: utf-8 -*-
from app import utils
from app.model import Base
from app.model.Base import STATUS_INVALID, STATUS_VALID
from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn

from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.flask_utils import FlaskDB
from datetime import datetime


# 学生管理
class Student(Base.BaseModel):
    class Meta:
        db_table = 'student' 

    uid = CharField()    
    nickname = CharField()
    name = CharField()
    sex  = IntegerField()
    province = CharField()
    city = CharField()
    country = CharField()
    urgent_contactor = CharField()
    urgent_mobile = CharField()
    birthday = DateField(default='1970-01-01')
    education = CharField()    
    image_url = CharField()
    mentor_id = CharField()
    detailed = CharField()
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = IntegerField(default=STATUS_VALID)


def GetStudents(page_num, item_per_page):
    count = Student.select().where(Student.status == STATUS_VALID).count()
    students = []
    print("total record nums: %d" %count)
    #memList = [model_to_dict(mem) for mem in Student.select().order_by(Student.id).paginate(page_num, item_per_page)]
    for mem in Student.select().where(Student.status == STATUS_VALID).order_by(Student.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        students.append(m)

    return count, students


def SearchStudentByUid(uid):
    record = Student.get_or_none(Student.uid == uid, Student.status == STATUS_VALID)
    r = model_to_dict(record)
    r = utils.Time2Str(r)
    r = utils.Decimal2Str(r)
    return r


def GetStdInfoById(sid):
    stdinfo = dict()
    record = Student.get_or_none(Student.id == sid, Student.status == STATUS_VALID)
    if record:
        r = model_to_dict(record)
        r = utils.Time2Str(r)
        r = utils.Decimal2Str(r)
        stdinfo['name'] = r['name']
        stdinfo['uid'] = r['uid']
        stdinfo['id'] = r['id']
        stdinfo['nickname'] = r['nickname']
        stdinfo['sex'] = r['sex']
        stdinfo['urgent_contactor'] = r['urgent_contactor']
        stdinfo['urgent_mobile'] = r['urgent_mobile']
        stdinfo['birthday'] = r['birthday']

    return stdinfo


def SearchStudentByName(page_num, item_per_page,name):
    count = Student.select().where(Student.name == name, Student.status == STATUS_VALID).count()
    students = []
    #memList = [model_to_dict(mem) for mem in Student.select().order_by(Student.id).paginate(page_num, item_per_page)]
    for mem in Student.select().where(Student.name == name, Student.status == STATUS_VALID).order_by(Student.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        students.append(m)

    return count, students

def GetStudentsInfoByName(name):
    stdsInfo = []
    for mem in Student.select().where(Student.name == name, Student.status == STATUS_VALID).order_by(Student.id):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        std_name_mobile = m['name'] + '_' + m['urgent_mobile']
        stdInfo = {'value':m['id'], 'label':std_name_mobile }
        stdsInfo.append(stdInfo)

    return stdsInfo


# create student 
def CreateStudent(mDict):
    errcode = 1
    print("will create a new record")
    print(mDict)
    m = dict_to_model(Student, mDict)
    m.save()
    mem = Student.get_or_none(Student.nickname == mDict['nickname'], Student.status == STATUS_VALID)
    if mem:
        errcode = 0
    return errcode

def UpdateStudentByUid(mDict):
    errcode = 1
    m = Student.update(**mDict).where(Student.uid==mDict['uid']).execute()
    if m == 1:
        errcode = 0
    return errcode

def DeleteStudentByUid(uid,status=STATUS_INVALID):
    # 0 mean delete successfully
    errcode = 1
    m = Student.update(status=status).where(Student.uid==uid).execute()
    if m == 1:
        errcode = 0
    return errcode



if __name__ == '__main__':
    pass
    """
    create_table()
    for i in range(15):
        Insertstudent()
    #InsertStudent()
    #InsertUser()

    #for i in range(1,4):
    #    Getstudents(i, 5)
     
    # query student by student id
    mem = SearchstudentById(901527124)
    if mem:
        #print(mem)
        print('%d'%mem.id + "  " + mem.name)
    else:
        print("cannot find this student")


    # query student by memmber name, there may exit many records
    memList = SearchstudentByName('孙宇')
    if memList:
        for mem in memList:
            print("id: %d"%mem.id + "  studentid:%d"%mem.studentid + "  name:" + mem.name)
    else:
        print("cannot find any records")

    # delete a student
    #DeletestudentById(45481440)


    # update a memeber  
    #UpdatestudentById(92596066)
    count, memItems = Getstudents(1, 5) 
    print("total is : %d"%count)
    print(memItems)   
    """
