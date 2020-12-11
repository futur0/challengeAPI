from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
db = SQLAlchemy()


class JackPotIndex(db.Model):
    __tablename__ = 'jackpotindex'
    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.String(80), unique=True, nullable=True)
    instance_name = db.Column(db.String(80), unique=False, nullable=True)
    drop_amount = db.Column(db.Float(), unique=False, nullable=True)
    data = db.Column(db.Float(), unique=False, nullable=True)
    is_closed = db.Column(db.Boolean, nullable=False, default=False)
    last_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    indexed_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notified = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<JackPotIndex %r>' % self.instance_name


class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    emails = db.Column(db.String(800), unique=False, nullable=True, default='')
    epic_threshold = db.Column(db.Float(), unique=False, nullable=True, default='')
    major_threshold = db.Column(db.Float(), unique=False, nullable=True, default='')
    minor_threshold = db.Column(db.Float(), unique=False, nullable=True, default='')

    def __repr__(self):
        return '<Settings %r>' % self.emails
