# -*- coding: utf-8 -*-
import json


def test_login(test_client):
    """
    GIVE a flask application
    WHEN the '/login' is requested(POST)
    THEN check the response is valid
    """
    userInfo = json.dumps({'username':'admin', 'password':111})
    response = test_client.post('/api/v1/users/login', data=userInfo)
    assert response.status_code == 200