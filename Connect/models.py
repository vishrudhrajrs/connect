from datetime import datetime
from Connect import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(length=40), unique=True, nullable=False)
    name = db.Column(db.String(length=30), nullable=False)
    employer = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(length=200), nullable=False)
    posts = db.relationship("Post", backref="owned_user", lazy=True)

    def __repr__(self):
        return str('Name '+str(self.name)) 



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jobname = db.Column(db.String(length=40), nullable=False)
    salary = db.Column(db.Integer,nullable=False)
    info = db.Column(db.String(length=1040), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey("users.id"))
    photo = db.Column(db.String(length=100), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)