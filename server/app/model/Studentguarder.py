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
        db_table = 'studentguarder' 

    student_id = IntegerField()
    member_id = IntegerField()
    relationship = IntegerField()
    focus = IntegerField()
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    status = IntegerField(default=STATUS_VALID)


# create Studentguarder 
def CreateStudentguarder(mDict):
    print("will create studentguarder")
    print(mDict)
    record = dict_to_model(Studentguarder, mDict)
    record.save()
    return 0

def GetStdIdByMemid(mid):
    stdids = []
    #memList = [model_to_dict(mem) for mem in Member.select().order_by(Member.id).paginate(page_num, item_per_page)]
    for rec in Studentguarder.select().where(Studentguarder.member_id == mid,Studentguarder.status == STATUS_VALID):
        r = model_to_dict(rec)
        r = utils.Time2Str(r)
        r = utils.Decimal2Str(r)
        stdids.append(r['student_id'])

    return stdids


def GetStdsByMemid(mid):
    stds = []
    #memList = [model_to_dict(mem) for mem in Member.select().order_by(Member.id).paginate(page_num, item_per_page)]
    for rec in Studentguarder.select(Studentguarder.member_id, Studentguarder.student_id, Studentguarder.relationship).where(Studentguarder.member_id == mid,Studentguarder.status == STATUS_VALID):
        r = model_to_dict(rec)
        stds.append(r)

    return stds

def DelStdGuardByMemidStdid(memid, stdid=None):
    if stdid == None:
        nums = Studentguarder.delete().where(Studentguarder.member_id == memid).execute()
    else:
        nums = Studentguarder.delete().where(Studentguarder.member_id == memid,Studentguarder.student_id == stdid).execute()
    return nums


if __name__ == '__main__':
    pass
