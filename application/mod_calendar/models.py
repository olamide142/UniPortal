import uuid
import random
from application import db 
from datetime import datetime

# Define a Calendar model
class Calendar(db.Model):

    __tablename__ = 'calendar'
        
    calendar_id           = db.Column(db.String(10),  nullable=False, primary_key=True)
    calendar_owner_id     = db.Column(db.String(40), nullable=False) # username of the owner if this calendar
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, calendar_owner_id):

        self.calendar_id                = gen_random_id()
        self.calendar_owner_id          = calendar_owner_id
        self.created_on                 = datetime.utcnow()

    def __repr__(self):
        return '<Calendar %r>' % (self.calendar_id)   

    


# Define a ClassRoom model
class Event(db.Model):

    __tablename__ = 'event'
        
    event_id            = db.Column(db.String(10),  nullable=False, primary_key=True)
    event_creator_id    = db.Column(db.String(40), nullable=False)
    date_n_time         = db.Column(db.DateTime, nullable=False)
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, event_creator_id, date_n_time):

        self.event_id                   = gen_random_id()
        self.event_id                   = event_creator_id
        self.date_n_time                = date_n_time
        self.created_on                 = datetime.utcnow()

    def __repr__(self):
        return f'<Event {self.event_id} - {self.event_id}>'


def gen_random_id(self):
    let = 'abcdefghijklmnopqrstuvwxyz1234567890'
    li = []
    for _ in range(7):
        li.append(let[random.randint(0, len(let)-1)])
    return "".join(li)
