import pytest
from application.mod_auth.models import User
from application.test_setup import client
from application import db, app
from flask_wtf.csrf import generate_csrf


def test_create_assessment(client):
    # when everything is done right
    file = open("demofile.pdf", "r")
    payload = {'title':'Test Assessment Title', 'description':'lorem ipsum blah blah blah', \
        'file':file, 'due_date':'(2020, 10, 30)', 'due_time':'(8, 48, 7, 189496)'}
    res = client.post('/assessment/create/xyz123/', data=payload)    
    assert 'Assessment Created Successfully' in str(res.data)
    # if form is incorrect
    file = open("demofile.pdf", "r")
    payload = {'title':'Test Assessment Title', 'file':file, \
    'due_date':'(2020, 10, 30)', 'due_time':'(8, 48, 7, 189496)'}
    res = client.post('/create/xyz123/', data=payload)    
    assert 'Form is Invalid Successfully' in str(res.data)


def test_get_assessments(client):
    # when everything is done right
    res = client.get('/assessment/list/xyz123/')    
    assert 'Test Assessment Title' in str(res.data)

def test_update_score(client):
    payload = {'score': 70, 'remark':'Great Job Keep it up'}
    res = client.post('/assessment/erf456/update_score/', data=payload)    
    assert 'Scores Updated' in str(res.data)
    # if form is incorrect
    payload = {'score': 70}
    res = client.post('/assessment/erf456/update_score/', data=payload)    
    assert 'Form is Invalid Updated' in str(res.data)





    

# def test_signin(client):
#     # when everything is done right
#     payload = {'username':'test', 'password':'123'}
#     res = client.post('/auth/signin/', data=payload)    
#     assert 'Logged in Successfully.' in str(res.data)

#     # if login information is incorrect
#     payload = {'username':'test', 'password':'1234'}
#     res = client.post('/auth/signin/', data=payload)    
#     assert 'Username or Password was incorrect.' in str(res.data)

#     # if form is incorrect
#     payload = {'username':'test'}
#     res = client.post('/auth/signin/', data=payload)    
#     assert 'Form submitted was invalid' in str(res.data)



# def test_signout(client):
#     # when everything is done right
#     res = client.post('/auth/signin/', \
#         data={'username':'test', 'password':'123'})    
#     assert 'Logged in Successfully.' in str(res.data)
    
#     res = client.get('/auth/signout/')  
#     assert 'Successfully Logged Out' in str(res.data)

#     # prevent an un-authenticated user from 
#     # login_required protected views 
#     res = client.get('/auth/see/', follow_redirects=True)  
#     assert 'Please log in to access this page' in str(res.data)

