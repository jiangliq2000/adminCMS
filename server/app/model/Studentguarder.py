# -*- coding: utf-8 -*-
from app import utils
from app.model import Base
from app.model.Base import STATUS_INVALID, STATUS_VALID
from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn

from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.flask_utils import FlaskDB
from datetime import datetime


# 学生会员关系表
class Studentguarder(Base.BaseModel):
    class Meta:
        db_table = 'Studentguarder' 

    student_id = IntegerField()
    member_id = IntegerField()
    relationship = IntegerField()
    focus = IntegerField()
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = IntegerField(default=STATUS_VALID)


# create Studentguarder 
def CreateStudentguarder(mDict):
    record = dict_to_model(Studentguarder, mDict)
    record.save()
    return 0



if __name__ == '__main__':
    pass
