import pytest
from application import app, db
from application.mod_auth.models import User
from application.tests.test_application import client
from application.mod_module.models import Module, ClassRoom

def test_create_module(client):
    # when everything is done right
    user = User(username='test007', email='test007@portal.com', \
        first_name='test007', last_name = 'testmi6', password='123')
    db.session.add(user)
    db.session.commit()
    module_url = 'http://127.0.0.1:8080/module/create/'
    payload = {'name':'Module Two Test', 'session':'2019JAN',
                'description': 'Test description data and many more',
                'code': 'MTT2020'}
    res = client.post('/module/create/', data=payload, follow_redirects=True)    
    assert 'Module Two Test' in str(res.data)
    assert '2019JAN' in str(res.data)
    # if a form field is not included
    payload = {'session':'2019JAN','description':'Test description data and many more',
                'code': 'MTT2020'}
    res = client.post('/module/create/', data=payload, follow_redirects=True)    
    assert 'Something went wrong, please try again' in str(res.data)


def test_view_module(client):
    # get module object
    module = Module.query.first()

    res = client.get(f'/module/view/{module.module_id}/')
    assert str(module.module_id) in str(res.data)
    assert str(module.module_code) in str(res.data)


def test_add_student(client):
    # import flask_login
    # assert 'orange' in str(flask_login.current_user)
    # # Create a student User Accounts
    # student = User(username='test3', email='test3@portal.com', \
    #     first_name='test333', last_name = 'test33', password='123')
    # db.session.add(student)
    # db.session.commit()

    # url = 'http://127.0.0.1:8080/module/0sxczb6/add/'
    # payload = {'username':'testuser2'}
    # r = s.post(url, data=payload)

    # assert 'Notification will be sent to the student' in str(res.data)

    pass 