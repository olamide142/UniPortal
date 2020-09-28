from application import db 
from datetime import datetime
import uuid

# Define a Module model
class Module(db.Model):

    __tablename__ = 'module'
        
    module_id    = db.Column(db.String(40),  nullable=False, primary_key=True)
    module_name   = db.Column(db.String(250), nullable=False)
    module_tutor_id = db.Column(db.String(40), nullable=False)
    session    = db.Column(db.String(20), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, module_name, module_tutor_id, session):

        self.module_id          = str(uuid.uuid4()) 
        self.module_name        = module_name
        self.module_tutor_id    = module_tutor_id
        self.session            = session
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return '<Module %r>' % (self.module_name)   

