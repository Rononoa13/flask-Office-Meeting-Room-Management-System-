from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SetMetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    availability = db.Column(db.Boolean, default=True)