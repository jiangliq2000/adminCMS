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
class Lesson(CourseDBBase.CourseBaseModel):
    class Meta:
        db_table = 'lesson' 

    course_id = IntegerField()
    lessonname = CharField()
    description = CharField()
    abilities = CharField()
    duration = IntegerField()
    homework = CharField()
    material_id = CharField()
    version = CharField()
    createtime = DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sequence = IntegerField()


def GetLessons(page_num, item_per_page):
    count = Lesson.select().count()
    lessons = []
    for mem in Lesson.select().order_by(Lesson.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        lessons.append(m)

    return count, lessons

"""
def SearchCourseByName(cname):
    mem = Lesson.get_or_none(Lesson.name == cname, Lesson.status == STATUS_VALID)
    m = model_to_dict(mem)
    m = utils.Time2Str(m)
    m = utils.Decimal2Str(m)
    return m
"""

def SearchLessonByName(page_num, item_per_page,name):
    count = Lesson.select().where(Lesson.lessonname == name).count()
    lessons = []
    for mem in Lesson.select().where(Lesson.lessonname == name).order_by(Lesson.id).paginate(page_num, item_per_page):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        lessons.append(m)

    return count, lessons

def GetLessonsByName(name):
    lessons = []
    for mem in Lesson.select().where(Lesson.lessonname.contains(name)):
        m = model_to_dict(mem)
        m = utils.Time2Str(m)
        m = utils.Decimal2Str(m)
        lessons.append(m)

    return lessons

# create lesson 
def CreateLesson(mDict):
    errcode = 1
    m = dict_to_model(Lesson, mDict)
    m.save()
    mem = Lesson.get_or_none(Lesson.lessonname == mDict['lessonname'])
    if mem:
        errcode = 0
    return errcode

def UpdateLessonByName(mDict):
    errcode = 1
    m = Lesson.update(**mDict).where(Lesson.lessonname==mDict['lessonname']).execute()
    if m == 1:
        errcode = 0
    return errcode

def UpdateCidByLid(cid,lid):
    errcode = 1
    m = Lesson.update(course_id=cid).where(Lesson.id==lid).execute()
    if m == 1:
        errcode = 0
    return errcode


def DeleteCourseByname(name):
    # 0 mean delete successfully
    errcode = 1
    m = Lesson.delete().where(Lesson.lessonname == name).execute()
    if m == 1:
        errcode = 0
    return errcode

def GetLessonsByCourseid(courseid):
    lessons = []
    for rec in Lesson.select().where(Lesson.course_id == courseid):
        r = model_to_dict(rec)
        r = utils.Time2Str(r)
        r = utils.Decimal2Str(r)
        lessons.append(r)
    return lessons

def GetLessonsBylessonid(lessonid):
    lesson = Lesson.get_or_none(Lesson.id == lessonid)
    if lesson:
        lesson = model_to_dict(lesson)
        lesson = utils.Time2Str(lesson)
        lesson = utils.Decimal2Str(lesson)
    return lesson

if __name__ == '__main__':
    pass
