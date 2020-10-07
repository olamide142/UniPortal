import uuid
import random
from application import db 
from datetime import datetime

# Define a Todo model
class Todo(db.Model):

    __tablename__ = 'todo'
        
    todo_id             = db.Column(db.String(10),  nullable=False, primary_key=True)
    owner_id            = db.Column(db.String(20), nullable=False)
    content             = db.Column(db.Text, nullable=False)
    status              = db.Column(db.String(15), nullable=False)
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, owner_id, content, status):

        self.todo_id            = str(uuid.uuid4())
        self.owner_id           = owner_id
        self.content            = content  
        self.status             = status
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return '<Todo %r>' % (self.todo_id)