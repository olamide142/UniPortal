import os
import tempfile
import pytest
from application import app, db
import config 
from application.mod_auth.models import User


@pytest.fixture
def client():

        
    app.config["TESTING"] = True
    app.testing = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client



def test_answer(client):
    assert "ONE" == 'one'.upper() # for debugging