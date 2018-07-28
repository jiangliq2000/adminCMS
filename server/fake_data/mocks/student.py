# -*- coding: utf-8 -*-

from faker import Faker
import json

def obj2dict(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startwith('__') and not callable(value):
            pr[name] = value

    return pr


def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj




class Student(object):
    """ mock to produce member information """
    def __init__(self):
        f = Faker('zh_CN')
        self.uid = f.uuid4()
        self.name = f.name()
        self.nickname = f.user_name()
        self.sex = f.random_int(min=1, max=2)
        self.province = f.province()
        self.city = f.city_suffix()
        self.country = f.country()        
        self.urgent_contactor = f.name()
        self.urgent_mobile = f.phone_number()
        self.birthday = f.date()
        self.education = f.word()
        self.image_url = f.image_url()
        self.mentor_id = f.user_name()
        self.detailed = f.word()
        self.createtime = f.date_time()        
        self.status = 1

	
		
    def toDict(self):
        return dict((name, getattr(self,name)) for name in dir(self) \
                   if not name.startswith('__') and not callable(getattr(self,name)))

        """
        return {'id':self.id, 'name':self.name, 'grade':self.grade, 'balance':self.balance, \
                'phone':self.phone, 'growth':self.growth, 'school':self.school, \
                'studentInfo':self.studentInfo, 'createTime':self.createTime \
               }
        """

    
if __name__ == '__main__':
    pass