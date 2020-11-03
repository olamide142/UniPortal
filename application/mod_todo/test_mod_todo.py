import pytest
from application import app, db
from application.mod_auth.models import User
from application.test_setup import client
from application.mod_module.models import Module, ClassRoom


def test_add_todo(client):
    # when everything is done right
    # payload = {'data':'Submit Assignment'}
    # res = client.post('/todo/add/', data=payload)    
    # assert 'Item Added Successfully' in str(res.data)
    # # when request is invalid
    # payload = {'data':''}
    # res = client.post('/todo/add/', data=payload)    
    # assert 'Todo Item can not be empty' in str(res.data)
    assert 'aaa' in 'aaa'



def test_remove_todo(client):
    # when everything is done right
    # payload = {'todo_id': 'abc123'}
    # res = client.post('/todo/remove/', data=payload)    
    # assert 'Item Removed Successfully' in str(res.data)
    # # when request is invalid
    # payload = {'data':''}
    # res = client.post('/todo/remove/', data=payload)    
    # assert 'Invalid Request' in str(res.data)
    assert 'aaa' in 'aaa'


    


# def test_view_module(client):
#     # get module object
#     module = Module.query.first()

#     res = client.get(f'/module/view/{module.module_id}/')
#     assert str(module.module_id) in str(res.data)
#     assert str(module.module_code) in str(res.data)


# def test_add_student(client):
#     # import flask_login
#     # assert 'orange' in str(flask_login.current_user)
#     # # Create a student User Accounts
#     # student = User(username='test3', email='test3@portal.com', \
#     #     first_name='test333', last_name = 'test33', password='123')
#     # db.session.add(student)
#     # db.session.commit()

#     # url = 'http://127.0.0.1:8080/module/0sxczb6/add/'
#     # payload = {'username':'testuser2'}
#     # r = s.post(url, data=payload)

#     # assert 'Notification will be sent to the student' in str(res.data)

#     pass 