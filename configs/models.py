from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
db = SQLAlchemy()


class JackPotDataHistory(db.Model):
    __tablename__ = 'jackpotdatahistory'

    id = db.Column(db.Integer, primary_key=True)

    epic_data = db.Column(db.Float(), unique=False, nullable=True)
    major_data = db.Column(db.Float(), unique=False, nullable=True)
    minor_data = db.Column(db.Float(), unique=False, nullable=True)

    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    jack_pot_data = db.Column(db.Integer, db.ForeignKey('jackpotdata.id'), nullable=False)
    jackpotdata = db.relationship('JackPotData', backref=db.backref('jackpotdata', lazy=True))


class JackPotData(db.Model):
    __tablename__ = 'jackpotdata'
    id = db.Column(db.Integer, primary_key=True)

    epic_data = db.Column(db.Float(), unique=False, nullable=True)
    major_data = db.Column(db.Float(), unique=False, nullable=True)
    minor_data = db.Column(db.Float(), unique=False, nullable=True)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    index_id = db.Column(db.Integer, db.ForeignKey('jackpotindex.id'),
                         nullable=False)
    jackpotindex = db.relationship('JackPotIndex',
                                   backref=db.backref('jackpotindex', lazy=True))

    # index_id = db.Column(db.Integer, db.ForeignKey('JackPotIndex.id'), nullable=False)
    # JackPotIndex = db.relationship('JackPotIndex', backref=db.backref('jackpot', lazy=True))

    def __repr__(self):
        return '<JackPotData %r>' % self.index_id


class JackPotIndex(db.Model):
    __tablename__ = 'jackpotindex'
    id = db.Column(db.Integer, primary_key=True)
    instance_epic = db.Column(db.String(80), unique=True, nullable=True)
    instance_major = db.Column(db.String(80), unique=True, nullable=True)
    instance_minor = db.Column(db.String(80), unique=True, nullable=True)
    drop_amount_epic = db.Column(db.Float(), unique=False, nullable=True)
    drop_amount_major = db.Column(db.Float(), unique=False, nullable=True)
    drop_amount_minor = db.Column(db.Float(), unique=False, nullable=True)
    indexed_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return '<JackPotIndex %r>' % self.indexed_date
