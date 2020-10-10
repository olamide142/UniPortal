import uuid
import random
from application import db 
from datetime import datetime

# Define a Board model
class Board(db.Model):

    __tablename__ = 'board'
        
    board_id            = db.Column(db.String(10),  nullable=False, primary_key=True)
    owner_id            = db.Column(db.String(20), nullable=False)
    board_name          = db.Column(db.String(50), nullable=False)
    file_name           = db.Column(db.String(10), nullable=False)
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, owner_id, board_name):

        self.board_id           = gen_random_id()
        self.owner_id           = owner_id
        self.board_name         = board_name
        self.file_name          = f'{gen_random_id()}.txt'
        self.created_on         = datetime.utcnow()

        #  Include this board to current user's pinboard
        pb = PinBoard(self.owner_id, self.board_id)
        db.session.add(pb)
        db.session.commit()

    def __repr__(self):
        return f'<Board {self.board_id} - {self.board_name}>'




class PinBoard(db.Model):

    __tablename__ = 'pinboard'
        
    pinboard_id            = db.Column(db.String(10),  nullable=False, primary_key=True)
    board_id               = db.Column(db.String(20), nullable=False)
    username               = db.Column(db.String(50), nullable=False)
    created_on             = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, username, board_id):

        self.pinboard_id        = gen_random_id()
        self.username           = username
        self.board_id           = board_id
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return f'<PinBoard {self.pinboard_id} - {self.usernmae}>'


def gen_random_id():
    let = 'abcdefghijklmnopqrstuvwxyz1234567890'
    li = []
    for _ in range(10):
        li.append(let[random.randint(0, len(let)-1)])
    return "".join(li)
