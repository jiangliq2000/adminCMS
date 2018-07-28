# -*- coding: utf-8 -*-
from app import utils
from app.model import CourseDBBase
from app.model.CourseDBBase import STATUS_INVALID, STATUS_VALID
from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn

from playhouse.shortcuts import model_to_dict, dict_to_model
#from playhouse.flask_utils import FlaskDB
from datetime import datetime


# 套餐关联教师管理
class Courseteacher(CourseDBBase.CourseBaseModel):
    class Meta:
        db_table = 'courseteacher' 

    course_id = IntegerField()
    teacher_id = IntegerField()
    teacher_name = CharField()
    teacher_mobile = CharField()
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# create courseteacher 
def CreateCourseteacher(mDict):
    cteacher = dict_to_model(Courseteacher, mDict)
    cteacher.save()
    return 0


def DeleteByCourseid(cid):
    # 0 mean delete successfully
    errcode = 1
    m = Courseteacher.delete().where(Courseteacher.course_id == cid).execute()
    if m == 1:
        errcode = 0
    return errcode

def GetTeacherByCourseid(courseid):
    teachers = []
    for rec in Courseteacher.select().where(Courseteacher.course_id == courseid):
        r = model_to_dict(rec)
        r = utils.Time2Str(r)
        r = utils.Decimal2Str(r)
        teachers.append(r)
    return teachers

if __name__ == '__main__':
    pass
