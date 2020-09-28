import os
import tempfile
import pytest
from application import app, db
import config 
from application.mod_auth.models import User
import json


@pytest.fixture
def client():

        
    app.config["TESTING"] = True
    app.testing = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(username='olamide', email="toothferry@portal.com", password="password")
        db.session.add(user)
        db.session.commit()
        u = User.query.all()
        assert len(u) == 1
    yield client


def func(client):
    return client.get('/auth/signin', follow_redirects=True)

def test_answer(client):
    from application.mod_auth.models import User
    li = []
    for i in User.query.all():
        li.append(i.email)
    assert b'toothferry' in func(client).data