# -*- coding: utf-8 -*-

from app.model import Studentguarder
from app.model.Base import STATUS_INVALID, STATUS_VALID

def test_new_studentguarder():
    """
    GIVEN a Studentguarder model
    WHEN a new Studentguarder is created
    THEN check the student_id, member_id, relationship
    """
    dataDict = {'student_id':11, 'member_id':22, 'relationship':3, 'focus':1}
    Studentguarder.CreateStudentguarder(dataDict)
    new_studguard = Studentguarder.get(student_id == 11)
    assert new_studguard.member_id == 22
    assert new_studguard.relationship == 3
