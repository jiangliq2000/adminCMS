# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn
import datetime
import json

from mocks import administrator as AdministratorMock
from playhouse.shortcuts import model_to_dict, dict_to_model


STATUS_VALID = 1
STATUS_INVALID = 0



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


# 机构管理
class Administrator(BaseModel):
    class Meta:
        db_table = 'administrator' 

    username = CharField()
    password = CharField()
    role = IntegerField()
    options = CharField()
    name = CharField()
    sex  = IntegerField() 
    province = CharField()
    city = CharField()
    country = CharField()
    mobile = CharField()    
    email = CharField()
    birthday = DateField(default='1970-01-01')
    education = CharField()
    lastloginip = CharField()
    lastdevice = CharField()
    lastlogintime = DateTimeField()
    status = IntegerField(default=STATUS_VALID)


# 建表
def create_table():
    print("will create a table")
    db.connect()
    db.create_tables([Administrator])
    print("create table done ...")

def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


# insert Teacher 
def InsertAdministrator():
    r_fake = AdministratorMock.Administrator()
    r_fake_dict = dict((name, getattr(r_fake,name)) for name in dir(r_fake) if not name.startswith('__') and not callable(getattr(r_fake,name)))
    r = dict_to_model(Administrator, r_fake_dict)
    r.save()



if __name__ == '__main__':
    
    create_table()
    for i in range(2):
        InsertAdministrator()
