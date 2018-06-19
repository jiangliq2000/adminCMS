# -*- coding: utf-8 -*-

from app import utils
from app.model import Base
from app.model.Base import STATUS_INVALID, STATUS_VALID
from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn

from playhouse.shortcuts import model_to_dict, dict_to_model

from datetime import datetime


# 机构管理
class Administrator(Base.BaseModel):
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



def GetRecordByUsername(username):
    return Administrator.get_or_none(Administrator.username == username, Administrator.status == STATUS_VALID)
    

def IsExistId(userid):
    return Administrator.get_or_none(Administrator.id == userid, Administrator.status == STATUS_VALID)


def UpdateRecrodByUsername(mDict):
    Administrator.update(**mDict).where(Administrator.username==mDict['username']).execute()