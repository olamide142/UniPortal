from application import db 
from datetime import datetime
import uuid
from werkzeug.security import check_password_hash, generate_password_hash





class AssessmentQuestion(db.Model):

    __tablename__ = 'assessmentquestion'

    aq_id                    = db.Column(db.String(40),  nullable=False, primary_key=True)
    module_id                = db.Column(db.String(15), nullable=False)
    title                    = db.Column(db.Text, nullable=False)
    file_id                  = db.Column(db.String(10),  nullable=False, unique=True)
    description              = db.Column(db.Text,  nullable=False, unique=True)
    due_date                 = db.Column(db.DateTime, nullable=False)
    created_on               = db.Column(db.DateTime, nullable=False)


    def __init__(self, title, file_id, module_id, description, due_date):

        self.aq_id                        = str(uuid.uuid4()) 
        self.description                  = description
        self.title                        = title
        self.file_id                      = file_id
        self.module_id                    = module_id
        self.due_date                     = due_date
        self.created_on                   = datetime.utcnow()

    def __repr__(self):
        return f'{self.aq_id} - {self.title}'





class Assessment(db.Model):

    __tablename__ = 'assessment'

    assessment_id    = db.Column(db.String(40),  nullable=False, primary_key=True)
    username         = db.Column(db.String(15), nullable=False)
    file_id          = db.Column(db.String(10),  nullable=False, unique=True)
    module_id        = db.Column(db.String(10),  nullable=False, unique=True)
    score            = db.Column(db.Integer,  nullable=True)
    remark           = db.Column(db.Text, nullable=True)
    created_on       = db.Column(db.DateTime, nullable=False)


    def __init__(self, username, file_id, module_id):

        self.assessment_id        = str(uuid.uuid4()) 
        self.username             = username
        self.file_id              = file_id
        self.module_id            = module_id
        self.created_on           = datetime.utcnow()

    def __repr__(self):
        return f'{self.assessment_id} - {self.username}'  

    