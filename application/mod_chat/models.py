from application import db 
from datetime import datetime
import random
import uuid

def gen_module_id():
    let = 'abcdefghijklmnopqrstuvwxyz1234567890'
    li = []
    for _ in range(7):
        li.append(let[random.randint(0, len(let)-1)])
    return "".join(li)



class Chat(db.Model):

    __tablename__ = 'chat'

    chat_id         = db.Column(db.String(10),  nullable=False, primary_key=True)
    user1           = db.Column(db.String(15), nullable=False)
    user2           = db.Column(db.String(15), nullable=False)
    created_on      = db.Column(db.DateTime, nullable=False)

    def __init__(self, user1, user2):

        self.chat_id        = gen_module_id()
        self.user1          = user1
        self.user2          = user2
        self.created_on     = datetime.utcnow()

    def __repr__(self):
        return f'{self.user1} - {self.user2}'




class Message(db.Model):
    __tablename__ = 'message'

    message_id      = db.Column(db.String(40),  nullable=False, primary_key=True)
    chat_id         = db.Column(db.String(10), nullable=False)
    username        = db.Column(db.String(15), nullable=False)
    content         = db.Column(db.Text, nullable=False)
    created_on      = db.Column(db.DateTime, nullable=False)


    def __init__(self, chat_id, username, content):

        self.message_id     = str(uuid.uuid4())
        self.user1          = user1
        self.user2          = user2
        self.created_on     = datetime.utcnow()

    def __repr__(self):
        return f'{self.user1} - {self.user2}'





# class Group(db.Model):
#     __tablename__ = 'group'


#     group_id        = db.Column(db.String(40),  nullable=False, primary_key=True)
#     chat_id         = db.Column(db.String(10), nullable=False)
#     username        = db.Column(db.String(15), nullable=False)
#     content         = db.Column(db.Text, nullable=False)
#     created_on      = db.Column(db.DateTime, nullable=False)