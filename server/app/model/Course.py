# -*- coding: utf-8 -*-
from app import utils
from app.model import CourseDBBase
from app.model.CourseDBBase import STATUS_INVALID, STATUS_VALID
from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn

from playhouse.shortcuts import model_to_dict, dict_to_model
#from playhouse.flask_utils import FlaskDB
from datetime import datetime


# 套餐管理
class Course(CourseDBBase.CourseBaseModel):
    class Meta:
        db_table = 'course' 

    name = CharField()
    category = IntegerField() 
    age= IntegerField()
    scope = IntegerField()
    price = DecimalField(max_digits=12, decimal_places=2)
    director = CharField()
    expiretime = DateTimeField()
    status = IntegerField()
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    repeats = IntegerField()
    media_url = CharField()
    description = CharField()
    lesson_times = IntegerField(default=0)

# insert course 
def InsertCourse():
    pass

def GetCourses(page_num, item_per_page):
    count = Course.select().count()
    courses = []
    for mem in Course.select().order_by(Course.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        courses.append(m)

    return count, courses


def GetOneCourseByName(cname):
    #mem = Course.get_or_none(Course.name == cname, Course.status == STATUS_VALID)
    mem = Course.get_or_none(Course.name == cname)
    m = model_to_dict(mem)
    m = utils.Time2Str(m)
    m = utils.Decimal2Str(m)
    return m

def GetNameById(cid):
    #mem = Course.get_or_none(Course.name == cname, Course.status == STATUS_VALID)
    course = Course.get_or_none(Course.id == cid)
    if course:
        course = model_to_dict(course)

    return course['name'] if course else ""


def SearchCourseByName(page_num, item_per_page,name):
    count = Course.select().where(Course.name == name).count()
    courses = []
    for mem in Course.select().where(Course.name == name).order_by(Course.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        courses.append(m)

    return count, courses

# create course 
def CreateCourse(mDict):
    errcode = 1
    m = dict_to_model(Course, mDict)
    m.save()
    mem = Course.get_or_none(Course.name == mDict['name'])
    if mem:
        errcode = 0
    return errcode

def UpdateCourseByName(mDict):
    errcode = 1
    m = Course.update(**mDict).where(Course.name==mDict['name']).execute()
    if m == 1:
        errcode = 0
    return errcode

def DeleteCourseByname(name):
    # 0 mean delete successfully
    errcode = 1
    m = Course.delete().where(Course.name == name).execute()
    if m == 1:
        errcode = 0
    return errcode



if __name__ == '__main__':
    pass
