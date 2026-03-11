from models import db

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    tagline = db.Column(db.String, default='')
    credentials = db.Column(db.String, default='')
    bio = db.Column(db.String, default='')
    photo = db.Column(db.String, default='images/default-candidate.svg')
    highlights = db.Column(db.String, default='[]')
    plan_of_action = db.Column(db.String, default='')
    council = db.Column(db.String, nullable=False, default='ENSC')
    created_at = db.Column(db.String, default='2026-03-08')
    facebook = db.Column(db.String, default='')

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, default='')
    message = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, default=None)
