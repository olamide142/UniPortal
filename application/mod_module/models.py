import uuid
import random
from application import db 
from datetime import datetime

# Define a Module model
class Module(db.Model):

    __tablename__ = 'module'
        
    module_id           = db.Column(db.String(10),  nullable=False, primary_key=True)
    module_name         = db.Column(db.String(250), nullable=False)
    module_tutor_id     = db.Column(db.String(40), nullable=False)
    session             = db.Column(db.String(20), nullable=True)
    description         = db.Column(db.String(250), nullable=True)
    module_code         = db.Column(db.String(15), nullable=True)
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, module_name, module_tutor_id, session, description, module_code):

        self.module_id          = self.gen_module_id()
        self.module_name        = module_name
        self.module_tutor_id    = module_tutor_id
        self.session            = session
        self.description        = description
        self.module_code        = module_code
        self.created_on         = datetime.utcnow()


    def __repr__(self):
        return f'<Module {self.module_id}>'


    def gen_module_id(self):
        let = 'abcdefghijklmnopqrstuvwxyz1234567890'
        li = []
        for _ in range(7):
            li.append(let[random.randint(0, len(let)-1)])
        return "".join(li)



# Define a ClassRoom model
class ClassRoom(db.Model):

    __tablename__ = 'classroom'
        
    id                  = db.Column(db.String(10),  nullable=False, primary_key=True)
    module_id           = db.Column(db.String(10), nullable=True)
    member_username     = db.Column(db.String(15), nullable=True)
    created_on          = db.Column(db.DateTime, nullable=False)

    
    def __init__(self, module_id, member_username):

        self.id                 = str(uuid.uuid4())
        self.module_id          = module_id
        self.member_username    = member_username
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return f'<ClassRoom {self.module_id} - {self.member_username}>'