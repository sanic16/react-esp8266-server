from extensions import db
from datetime import datetime
import pytz

class Zone(db.Model):
    __tablename__ = 'zone'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    created_at = db.Column(db.DateTime(), nullable = False, default = datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable = False, default = datetime.now(pytz.timezone('America/Guatemala')), onupdate = datetime.now(pytz.timezone('America/Guatemala')))

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref = 'zones')

class SubZone(db.Model):
    __tablename__ = 'subzone'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')), onupdate=datetime.now(pytz.timezone('America/Guatemala')))

    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'), nullable = False)
    zone = db.relationship('Zone', backref = 'subzones')

class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')), onupdate=datetime.now(pytz.timezone('America/Guatemala')))
    status = db.Column(db.Boolean(), nullable=False, default=False)

    subzone_id = db.Column(db.Integer, db.ForeignKey('subzone.id'), nullable = False)
    subzone = db.relationship('SubZone', backref = 'devices')

    

