# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn
import datetime
import json

from mocks import student as StudentMock
from playhouse.shortcuts import model_to_dict, dict_to_model


STATUS_VALID = 1
STATUS_INVALID = 0



#db = MySQLDatabase(host='192.168.163.128', user='root', passwd='1', database='test', charset='utf8')
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


# 学生管理
class Student(BaseModel):
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
    createtime = DateTimeField()
    status = IntegerField(default=STATUS_VALID)


# 建表
def create_table():
    print("will create a table")
    db.connect()
    db.create_tables([Student])
    print("create table done ...")

def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


# insert Student 
def InsertStudent():
    r_fake = StudentMock.Student()
    r_fake_dict = dict((name, getattr(r_fake,name)) for name in dir(r_fake) if not name.startswith('__') and not callable(getattr(r_fake,name)))
    r = dict_to_model(Student, r_fake_dict)
    r.save()

def GetStudents(page_num, item_per_page):
    count = Student.select().count()
    print("total record nums: %d" %count)
    recList = []
    
    for record in Student.select().order_by(Student.id).paginate(page_num, item_per_page):
        recList.append(record)
        print("%d"%record.id + "  " + record.name)
    print(recList)   

def SearchStudentById(Studentuid):
    record = Student.get_or_none(Student.uid == Studentuid)
    return record


def SearchStudentByName(name):
    memList = []
    for mem in Student.select().where(Student.name == name):
        memList.append(mem)

    return memList

def UpdateStudentById(Studentuid):
    r_fake = StudentMock.Student()
    r_fake_dict = dict((name, getattr(r_fake,name)) for name in dir(r_fake) if not name.startswith('__') and not callable(getattr(r_fake, name)))
    print(r_fake_dict)
    r_fake_dict['Studentid'] = Studentid
    r = Student.update(**r_fake_dict).where(Student.uid==Studentuid).execute()
    print("m is ")
    print(r)
    if r == 1:
        print("update successfully")
    else:
        print("update failure")



def DeleteStudentById(Studentid):
    r = Student.update(status=0).where(Student.uid==Studentuid).execute()
    print("m is ")
    print(r)
    if r == 1:
        print("delete successfully")
    else:
        print("delete failure")



if __name__ == '__main__':
    
    create_table()
    for i in range(25):
        InsertStudent()
    """
    #InsertStudent()
    #InsertUser()

    #for i in range(1,4):
    #    GetStudents(i, 5)
     
    # query Student by Student id
    mem = SearchStudentById(901527124)
    if mem:
        #print(mem)
        print('%d'%mem.id + "  " + mem.name)
    else:
        print("cannot find this Student")


    # query Student by memmber name, there may exit many records
    memList = SearchStudentByName('孙宇')
    if memList:
        for mem in memList:
            print("id: %d"%mem.id + "  Studentid:%d"%mem.Studentid + "  name:" + mem.name)
    else:
        print("cannot find any records")
    """

    # delete a Student
    #DeleteStudentById(45481440)


    # update a memeber  
    #UpdateStudentById(92596066)
    #GetStudents(1,5)