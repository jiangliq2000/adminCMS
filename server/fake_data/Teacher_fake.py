# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn
import datetime
import json

from mocks import teacher as TeacherMock
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


# 教师管理
class Teacher(BaseModel):
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
    address = CharField()
    mobile = CharField()
    email = CharField()    
    birthday = DateField(default='1970-01-01')
    education = CharField()
    school_id = IntegerField()
    image_url = CharField()
    createtime = DateTimeField()
    status = IntegerField(default=STATUS_VALID)


# 建表
def create_table():
    print("will create a table")
    db.connect()
    db.create_tables([Teacher])
    print("create table done ...")

def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


# insert Teacher 
def InsertTeacher():
    r_fake = TeacherMock.Teacher()
    r_fake_dict = dict((name, getattr(r_fake,name)) for name in dir(r_fake) if not name.startswith('__') and not callable(getattr(r_fake,name)))
    r = dict_to_model(Teacher, r_fake_dict)
    r.save()

def GetTeachers(page_num, item_per_page):
    count = Teacher.select().count()
    print("total record nums: %d" %count)
    recList = []
    
    for record in Teacher.select().order_by(Teacher.id).paginate(page_num, item_per_page):
        recList.append(record)
        print("%d"%record.id + "  " + record.name)
    print(recList)   

def SearchTeacherById(Teacheruid):
    record = Teacher.get_or_none(Teacher.uid == Teacheruid)
    return record


def SearchTeacherByName(name):
    memList = []
    for mem in Teacher.select().where(Teacher.name == name):
        memList.append(mem)

    return memList

def UpdateTeacherById(Teacheruid):
    r_fake = TeacherMock.Teacher()
    r_fake_dict = dict((name, getattr(r_fake,name)) for name in dir(r_fake) if not name.startswith('__') and not callable(getattr(r_fake, name)))
    print(r_fake_dict)
    r_fake_dict['Teacherid'] = Teacherid
    r = Teacher.update(**r_fake_dict).where(Teacher.uid==Teacheruid).execute()
    print("m is ")
    print(r)
    if r == 1:
        print("update successfully")
    else:
        print("update failure")



def DeleteTeacherById(Teacherid):
    r = Teacher.update(status=0).where(Teacher.uid==Teacheruid).execute()
    print("m is ")
    print(r)
    if r == 1:
        print("delete successfully")
    else:
        print("delete failure")



if __name__ == '__main__':
    
    create_table()
    for i in range(3):
        InsertTeacher()
    """
    #InsertTeacher()
    #InsertUser()

    #for i in range(1,4):
    #    GetTeachers(i, 5)
     
    # query Teacher by Teacher id
    mem = SearchTeacherById(901527124)
    if mem:
        #print(mem)
        print('%d'%mem.id + "  " + mem.name)
    else:
        print("cannot find this Teacher")


    # query Teacher by memmber name, there may exit many records
    memList = SearchTeacherByName('孙宇')
    if memList:
        for mem in memList:
            print("id: %d"%mem.id + "  Teacherid:%d"%mem.Teacherid + "  name:" + mem.name)
    else:
        print("cannot find any records")
    """

    # delete a Teacher
    #DeleteTeacherById(45481440)


    # update a memeber  
    #UpdateTeacherById(92596066)
    #GetTeachers(1,5)
