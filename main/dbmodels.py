from main import db,login_manager
#UserMixin contains all the methods such as is_login, is_authenticated
from flask_login import UserMixin
from datetime import datetime
import pytz

#This is required to know that the user is active and logged in
#This sets the callback for reloading a user from the session.

@login_manager.user_loader
def load_user(details_id):
    return Details.query.get(int(details_id))


class Details(db.Model,UserMixin):
    def get_id(self):
        return(self.id)
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(length=30),nullable=False)
    email = db.Column(db.String(length=50),nullable=False,unique=True)
    password = db.Column(db.String(length=20),nullable=False)
    todos = db.relationship('Todo')

    def __repr__(self) -> str:
        return f"{self.email} is registered."

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(length=50),nullable=False,unique=True)
    description = db.Column(db.String,nullable=False)
    date_added = db.Column(db.DateTime,nullable=False,default= datetime.now(pytz.   timezone('Asia/Kathmandu')))
    details_id = db.Column(db.Integer,db.ForeignKey('details.id'))
