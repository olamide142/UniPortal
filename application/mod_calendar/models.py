import uuid
import random
from application import db 
from datetime import datetime

class Event(db.Model):

    __tablename__ = 'event'
        
    event_id            = db.Column(db.String(10),  nullable=False, primary_key=True)
    creator_id          = db.Column(db.String(40), nullable=False)
    module_id           = db.Column(db.String(40), nullable=False)
    title               = db.Column(db.Text, nullable=False)
    date_n_time         = db.Column(db.DateTime, nullable=False)
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, creator_id, title, module_id, date_n_time):

        self.event_id                   = gen_random_id()
        self.creator_id                 = creator_id
        self.title                      = title
        self.module_id                  = module_id
        self.date_n_time                = date_n_time
        self.created_on                 = datetime.utcnow()

    def __repr__(self):
        return f'<Event {self.event_id} - {self.event_id}>'


def gen_random_id():
    let = 'abcdefghijklmnopqrstuvwxyz1234567890'
    li = []
    for _ in range(7):
        li.append(let[random.randint(0, len(let)-1)])
    return "".join(li)



class NoEvent():
        
    event_id            = None
    creator_id          = None
    module_id           = None
    title               = None
    date_n_time         = None
    created_on          = None
    

