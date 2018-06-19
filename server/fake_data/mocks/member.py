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




class Member(object):
    """ mock to produce member information """
    def __init__(self):
        f = Faker('zh_CN')
        self.nickname = f.user_name()
        self.name = f.name()
        self.sex = f.random_int(min=1, max=2)
        self.address = f.street_address()
        self.province = f.province()
        self.city = f.city_suffix()
        self.country = f.country()
        self.wxunionid = f.isbn10()
        self.memtype = f.random_int(min=0, max=4)
        self.mobile = f.phone_number()
        self.email = f.email()
        self.birthday = f.date()
        self.education = f.word()
        self.industry = f.word()
        self.background = f.word()
        self.changetime = f.date_time()
        self.createtime = f.date_time()
        self.emailVerified = f.random_int(min=0, max=1)
        self.lastloginip = f.ipv4()
        self.lastdevice = f.word()
        self.lastlogintime = f.date_time()
        self.balance = f.pyfloat(left_digits=4, right_digits=2, positive=True)
        self.school_id = f.random_digit()
        self.inviter_id = f.random_digit()
        self.status = f.random_int(min=0, max=1)

        """
        students = {}
        students['student1'] = f.sentences()
        students['student2'] = f.sentences()
        self.studentInfo = students
        self.createTime = f.date()
        self.email = f.email()
        """
		
		
    def toDict(self):
        return dict((name, getattr(self,name)) for name in dir(self) \
                   if not name.startswith('__') and not callable(getattr(self,name)))

        """
        return {'id':self.id, 'name':self.name, 'grade':self.grade, 'balance':self.balance, \
                'phone':self.phone, 'growth':self.growth, 'school':self.school, \
                'studentInfo':self.studentInfo, 'createTime':self.createTime \
               }
        """


MemberList = []
for i in range(5):
    MemberList.append(Member().toDict())    
    
if __name__ == '__main__':
    MemberList = []
    for i in range(5):
        MemberList.append(Member().toDict())    
    print("mock member data as below")
    for i in range(len(MemberList)):
        print(MemberList[i])    
