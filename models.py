from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    user_role = db.relationship('UserRole', back_populates='user')

    def __str__(self):
        return self.user_role

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_role = db.Column(db.String(15))
    user_id = db.Column(db.ForeignKey("user.id"), nullable=False)
    user = db.relationship('User', back_populates='user_role')

class UserView(ModelView):
    form_columns = ['user_role', 'user']


class SetMeeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    owner = db.Column(db.Integer)