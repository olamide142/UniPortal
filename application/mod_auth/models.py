from application import db 
from datetime import datetime
import uuid
from werkzeug.security import check_password_hash, generate_password_hash

# Define a User model
class User(db.Model):

    __tablename__ = 'user'

    # User Name
    user_id    = db.Column(db.String(40),  nullable=False, primary_key=True)
    username   = db.Column(db.String(15), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    email    = db.Column(db.String(128),  nullable=False)
    password = db.Column(db.String(192),  nullable=False)
    role     = db.Column(db.String(10), nullable=False)
    # authenticated = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, nullable=False)


    # New instance instantiation procedure
    def __init__(self, username, email, password, first_name='', last_name='', role='Student'):

        self.user_id        = str(uuid.uuid4()) 
        self.username       = username
        self.first_name     = first_name
        self.last_name      = last_name
        self.email          = email
        self.password       = generate_password_hash(password)
        self.role           = role
        self.created_on     = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % (self.username)   

    def get_id(self):
        return self.username

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
