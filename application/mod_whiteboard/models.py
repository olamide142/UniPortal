import uuid
import random
from application import db 
from datetime import datetime

# Define a Board model
class Board(db.Model):

    __tablename__ = 'board'
        
    board_id            = db.Column(db.String(10),  nullable=False, primary_key=True)
    owner_id            = db.Column(db.String(20), nullable=False)
    file_name           = db.Column(db.String(10), nullable=False)
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, owner_id):

        self.board_id           = gen_random_id()
        self.owner_id           = owner_id
        self.file_name          = f'{gen_random_id()}.txt'
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return '<Board %r>' % (self.board_id)


    def gen_random_id(self):
        let = 'abcdefghijklmnopqrstuvwxyz1234567890'
        li = []
        for _ in range(10):
            li.append(let[random.randint(0, len(let)-1)])
        return "".join(li)
