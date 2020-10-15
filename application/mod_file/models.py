from application import db 
from datetime import datetime


def gen_module_id():
    let = 'abcdefghijklmnopqrstuvwxyz1234567890'
    li = []
    for _ in range(7):
        li.append(let[random.randint(0, len(let)-1)])
    return "".join(li)



class FileSystem(db.Model):

    __tablename__ = 'filesystem'

    file_id         = db.Column(db.String(10),  nullable=False, primary_key=True)
    file_name       = db.Column(db.String(250), nullable=False, unique=True)
    file_type       = db.Column(db.String(10), nullable=False)
    file_size       = db.Column(db.Integer, nullable=False)
    upload_by       = db.Column(db.String(15), nullable=False)
    created_on      = db.Column(db.DateTime, nullable=False)

    # New instance instantiation procedure
    def __init__(self, file_name, file_type, file_size, upload_by):

        self.file_id        = gen_module_id()
        self.file_name      = file_name
        self.file_type      = file_type
        self.file_size      = file_size
        self.upload_by      = upload_by
        self.created_on     = datetime.utcnow()

    def __repr__(self):
        return f'{self.file_name}'