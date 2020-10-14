import uuid
import random
from application import db 
from datetime import datetime


def gen_module_id():
    let = 'abcdefghijklmnopqrstuvwxyz1234567890'
    li = []
    for _ in range(7):
        li.append(let[random.randint(0, len(let)-1)])
    return "".join(li)



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

        self.module_id          = gen_module_id()
        self.module_name        = module_name
        self.module_tutor_id    = module_tutor_id
        self.session            = session
        self.description        = description
        self.module_code        = module_code
        self.created_on         = datetime.utcnow()


    def __repr__(self):
        return f'<Module {self.module_id}>'




class ClassRoom(db.Model):

    __tablename__ = 'classroom'
        
    id                  = db.Column(db.String(10),  nullable=False, primary_key=True)
    module_id           = db.Column(db.String(10), nullable=False)
    member_username     = db.Column(db.String(15), nullable=False)
    created_on          = db.Column(db.DateTime, nullable=False)

    
    def __init__(self, module_id, member_username):

        self.id                 = str(uuid.uuid4())
        self.module_id          = module_id
        self.member_username    = member_username
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return f'<ClassRoom {self.module_id} - {self.member_username}>'




class ModuleMaterial(db.Model):

    __tablename__       = 'modulematerial'
        
    material_id         = db.Column(db.String(10),  nullable=False, primary_key=True)
    sub_id              = db.Column(db.String(10), nullable=True)
    file_id             = db.Column(db.String(10), nullable=False)
    created_on          = db.Column(db.DateTime, nullable=False)

    
    def __init__(self, file_id, sub_id):

        self.material_id        = gen_module_id()
        self.sub_id             = sub_id
        self.file_id            = file_id
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return f'{self.material_id} - {self.file_id}'



class ModuleSub(db.Model):
    # Module Subcategory 
    __tablename__ = 'modulesub'
        
    sub_id              = db.Column(db.String(10),  nullable=False, primary_key=True)
    module_id           = db.Column(db.String(10), nullable=False)
    sub_name            = db.Column(db.String(250), nullable=False)
    description         = db.Column(db.Text, nullable=True)
    created_on          = db.Column(db.DateTime, nullable=False)

    
    def __init__(self, module_id, sub_name, description):

        self.sub_id             = gen_module_id()
        self.module_id          = module_id
        self.sub_name           = sub_name
        self.description        = description
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return f'{self.sub_id} - {self.sub_name}'


