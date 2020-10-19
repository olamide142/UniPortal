import pytest
from application.mod_auth.models import User
from application.test_setup import client
from application import db, app
from .forms import SignupForm
from flask_wtf.csrf import generate_csrf


# def test_signup(client):
#     # when everything is done right
#     payload = {'username':'test', 'email':'tes@portal.com', \
#         'first_name':'test', 'last_name':'test', 'password':'123'}
#     res = client.post('/auth/signup/', data=payload)    
#     assert 'Account Created Successfully' in str(res.data)

#     # if form is incorrect
#     payload = {'username':'test', 'first_name':'test', \
#         'last_name':'test', 'password':'123'}
#     res = client.post('/auth/signup/', data=payload)    
#     assert 'Form submitted was invalid' in str(res.data)

#     # if user tries to sign up with a already existing user's info
#     payload = {'username':'test', 'email':'tes@portal.com', \
#         'first_name':'test', 'last_name':'test', 'password':'123'}
#     res = client.post('/auth/signup/', data=payload)    
#     assert 'Account Creation was Unsuccessfull' in str(res.data)
    


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

