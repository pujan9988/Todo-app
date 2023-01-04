from main import db,login_manager,app
from time import time
#UserMixin contains all the methods such as is_login, is_authenticated
from flask_login import UserMixin

from datetime import datetime
import pytz,jwt

#itsdangerous is used to create secured timesensitive tokens

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
    todos = db.relationship('Todo',backref="author",lazy=True)

    #get_resest_token is a method to create a new token for the user
    def get_reset_token(self, expires_sec = 1800):
        return jwt.encode(
            {'reset_password':self.id, 'exp': time() +  expires_sec},
            app.config['SECRET_KEY'],algorithm='HS256'
        )

    #method to verify a token
    @staticmethod
    def verify_reset_token(token):
        try:
            id = jwt.decode(token,app.config['SECRET_KEY'],algorithms='HS256')['reset_password']
        except:
            return None
        return Details.query.get(id)
        
    def __repr__(self) -> str:
        return f"{self.email} is registered."

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(length=50),nullable=False)
    description = db.Column(db.String,nullable=False)
    date_added = db.Column(db.DateTime,nullable=False,default=datetime.now(pytz.timezone('Asia/Kathmandu')))
    details_id = db.Column(db.Integer,db.ForeignKey('details.id'))
