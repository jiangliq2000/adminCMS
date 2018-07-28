# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, BigIntegerField,CharField, BooleanField, \
                   DecimalField, IntegerField, TextField, DateField, DateTimeField, fn
from datetime import datetime
import json

from playhouse.shortcuts import model_to_dict, dict_to_model

db = MySQLDatabase(host='sh-cdb-j421jq38.sql.tencentcdb.com', port=63471,  user='root', passwd='Joyfulkid123', database='joy_coursedb', charset='utf8')


class CourseBaseModel(Model):
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



# 套餐管理
class Lesson(CourseBaseModel):
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


def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


def GetLessonsByName(name):
    lessons = []
    for mem in Lesson.select().where(Lesson.lessonname.contains(name)):
        m = model_to_dict(mem)
        #m = utils.Time2Str(m)
        #m = utils.Decimal2Str(m)
        lessons.append(m)
    return lessons





if __name__ == '__main__':

    # query member by memmber name, there may exit many records
    lessons = GetLessonsByName('模型')
    if lessons:
        for l in lessons:
            #print("id: %d"%l.id + "  course_id:%d"%l.course_id + "  name:" + l.name)
            print(l)
    else:
        print("cannot find any records")

