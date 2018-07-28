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




class Teacher(object):
    """ mock to produce member information """
    def __init__(self):
        f = Faker('zh_CN')
        self.name = f.name()
        self.password= f.password(length=8)
        self.options = "all"
        self.nickname = f.user_name()
        self.sex = f.random_int(min=1, max=2)
        self.province = f.province()
        self.city = f.city_suffix()
        self.country = f.country()
        self.address = f.street_address()
        self.mobile = f.phone_number()
        self.email = f.email()
        self.birthday = f.date()
        self.education = f.word()
        self.school_id = f.random_digit()
        self.image_url = f.image_url()
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