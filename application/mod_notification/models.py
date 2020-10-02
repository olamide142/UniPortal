import uuid
import random
from application import db 
from datetime import datetime

# Define a Notification model
class Notification(db.Model):

    __tablename__ = 'notification'
        
    notification_id     = db.Column(db.String(10),  nullable=False, primary_key=True)
    sender              = db.Column(db.String(20), nullable=False)
    receiver            = db.Column(db.String(20), nullable=False)
    notification_type   = db.Column(db.String(30), nullable=False)
    content             = db.Column(db.Text, nullable=True)
    seen                = db.Column(db.Boolean, nullable=True)
    created_on          = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, sender, receiver, notification_type, content):

        self.notification_id    = str(uuid.uuid4())
        self.sender             = sender
        self.receiver           = receiver  
        self.notification_type  = notification_type
        self.content            = content
        self.seen               = seen
        self.created_on         = datetime.utcnow()

    def __repr__(self):
        return '<Notification %r>' % (self.notification_id)