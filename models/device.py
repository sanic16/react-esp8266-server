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

    @classmethod
    def get_by_id(cls, zone_id):
        return cls.query.filter_by(id = zone_id).first()

    @classmethod
    def get_by_name(cls, zone_name):
        return cls.query.filter_by(name = zone_name).first()

    @classmethod
    def get_all(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all() 
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class SubZone(db.Model):
    __tablename__ = 'subzone'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')), onupdate=datetime.now(pytz.timezone('America/Guatemala')))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref = 'subzones')
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'), nullable = False)
    zone = db.relationship('Zone', backref = 'subzones')

    @classmethod
    def get_by_id(cls, subzone_id):
        return cls.query.filter_by(id = subzone_id).first()
    
    @classmethod
    def get_by_name(cls, subzone_name):
        return cls.query.filter_by(name = subzone_name).first()
    
    @classmethod
    def get_all(cls, user_id):
        return cls.query.filter_by(user_id = user_id).all()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')), onupdate=datetime.now(pytz.timezone('America/Guatemala')))
    status = db.Column(db.Boolean(), nullable=False, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref = 'devices')
    subzone_id = db.Column(db.Integer, db.ForeignKey('subzone.id'), nullable = False)
    subzone = db.relationship('SubZone', backref = 'devices')

    @classmethod
    def get_by_id(cls, device_id):
        return cls.query.filter_by(id = device_id).first()

    @classmethod
    def get_by_name(cls, device_name):
        return cls.query.filter_by(name = device_name).first()

    @classmethod
    def get_all(cls, user_id):
        return cls.query.filter_by(user_id = user_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.add(self)
        db.session.commit()

