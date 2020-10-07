import os
import tempfile
import pytest
from application import app, db
from application.mod_auth.models import User
import config 

@pytest.fixture
def client():

        
    app.config["TESTING"] = True
    app.testing = True
    config.CSRF_ENABLED = False
    config.WTF_CSRF_ENABLED = False

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client



def test_answer(client):
    assert "ONE" == 'one'.upper() # for debugging
