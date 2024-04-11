from extensions import db
from datetime import datetime
from models.device import Zone, SubZone, Device
import pytz


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')), onupdate=datetime.now(pytz.timezone('America/Guatemala')))
    zones = db.relationship('Zone', backref = 'user', cascade='all, delete-orphan')
    subzones = db.relationship('SubZone', backref = 'user', cascade='all, delete-orphan')
    devices = db.relationship('Device', backref = 'user', cascade='all, delete-orphan')


    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()  
    
    @classmethod
    def get_all_devices(cls, user_id):
        devices = (
            db.session.query(Device)
            .join(SubZone, SubZone.id == Device.subzone_id)
            .join(Zone, Zone.id == SubZone.zone_id)
            .join(User, User.id == Zone.user_id)
            .filter(User.id == user_id)
            .all()
        )
        return devices

    @classmethod
    def get_all_zones(cls, user_id):
        zones = (
            db.session.query(Zone)
            .join(User, User.id == Zone.user_id)
            .filter(User.id  == user_id)
            .all()
        )
        return zones

    def save(self):
        db.session.add(self)
        db.session.commit()
