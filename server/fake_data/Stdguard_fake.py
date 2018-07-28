# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn
from datetime import datetime
import json

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


# 学生家长表
class StdGuard(BaseModel):
    class Meta:
        db_table = 'studentguarder' 

    student_id = IntegerField()
    member_id = IntegerField()
    relationship = IntegerField()
    focus = IntegerField()
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = IntegerField(default=STATUS_VALID)


# 建表
def create_table():
    print("will create a table")
    db.connect()
    db.create_tables([StdGuard])
    print("create table done ...")

def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


# insert Teacher 
def InsertTeacher(i):
    r_fake_dict = {'member_id':i, 'student_id':i+9, 'focus':0, 'relationship':i%4+1}
    r = dict_to_model(StdGuard, r_fake_dict)
    r.save()

def DeleteByMemId(memid):
    StdGuard.delete().where(StdGuard.member_id == memid).execute()


if __name__ == '__main__':
    
    #create_table()
    DeleteByMemId(1)


