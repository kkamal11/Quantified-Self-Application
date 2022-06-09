from .database import db

class User(db.Model):
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(100), nullable=False)
    password=db.Column(db.String(100), nullable=False)
    users_tracker = db.relationship("Tracker",backref="user")

class Tracker(db.Model):
    tracker_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    tracker_name=db.Column(db.String(100), nullable=False)
    tracker_type=db.Column(db.String(100), nullable=False)
    tracker_description = db.Column(db.String(100))
    track_time = db.Column(db.DateTime)
    setting = db.Column(db.String)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    trackers_log = db.relationship("Logs",backref="tracker")

class Logs(db.Model):
    logs_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    log_time=db.Column(db.DateTime, nullable=False)
    value = db.Column(db.String)
    note=db.Column(db.String(100))
    tracker_id=db.Column(db.Integer, db.ForeignKey('tracker.tracker_id'))
#db.create_all()