from application import db 
from datetime import datetime
from application.mod_whiteboard.models import gen_random_id



# Define a Todo model
class Todo(db.Model):

    __tablename__ = 'todo'
        
    todo_id             = db.Column(db.String(10),  nullable=False, primary_key=True)
    owner_id            = db.Column(db.String(20), nullable=False)
    content             = db.Column(db.Text, nullable=False)
    status              = db.Column(db.String(15), nullable=False)
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, owner_id, content):

        self.todo_id            = gen_random_id()
        self.owner_id           = owner_id
        self.content            = content  
        self.status             = ""
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return f'<Todo {self.todo_id}>'