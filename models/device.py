from extensions import db
from datetime import datetime
from sqlalchemy import func
import pytz

class Zone(db.Model):
    __tablename__ = 'zone'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    created_at = db.Column(db.DateTime(), nullable = False, default = datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable = False, default = datetime.now(pytz.timezone('America/Guatemala')), onupdate = datetime.now(pytz.timezone('America/Guatemala')))

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable = False)
    subzones = db.relationship('SubZone', backref = 'zone', cascade='all, delete-orphan')


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
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'), nullable = False)
    devices = db.relationship('Device', backref = 'subzone', cascade='all, delete-orphan')


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
    endpoint = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    subzone_id = db.Column(db.Integer, db.ForeignKey('subzone.id'), nullable = False)
    device_status = db.relationship('DeviceStatus', backref = 'device', cascade='all, delete-orphan')

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
        db.session.delete(self)
        db.session.commit()


class DeviceStatus(db.Model):
    __tablename__ = 'device_status'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean(), nullable=False)
    is_error = db.Column(db.Boolean(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')))
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('America/Guatemala')), onupdate=datetime.now(pytz.timezone('America/Guatemala')))
    device_id = db.Column(db.Integer(), db.ForeignKey('device.id'), nullable=False)

    @classmethod
    def get_status_counts(cls, is_error=False):
        """
        Get the count of True and False values in the status column
        where is_error is equal to the provided value.

        Args:
        - is_error (bool): Filter condition for is_error column (default is False).

        Returns:
        - Tuple[int, int]: A tuple containing the count of True and False values.
        """
        true_count, false_count = db.session.query(
            func.sum(func.cast(cls.status == True, db.Integer)),
            func.sum(func.cast(cls.status == False, db.Integer))
        ).filter(cls.is_error == is_error).first()

        return true_count or 0, false_count or 0
    
    @classmethod
    def get_error_count(cls):
        """
        Get the count of errors (is_error == True).

        Returns:
        - int: The count of errors.
        """
        error_count = db.session.query(func.count()).filter(cls.is_error == True).scalar()

        return error_count or 0
    
    @classmethod
    def get_status_counts_by_device(cls, device_id, is_error=False):
        """
        Get the count of True and False values in the status column
        for the specified device_id where is_error is equal to the provided value.

        Args:
        - device_id (int): The ID of the device.
        - is_error (bool): Filter condition for is_error column (default is False).

        Returns:
        - Tuple[int, int]: A tuple containing the count of True and False values.
        """
        true_count, false_count = db.session.query(
            func.sum(func.cast(cls.status == True, db.Integer)),
            func.sum(func.cast(cls.status == False, db.Integer))
        ).filter(cls.is_error == is_error, cls.device_id == device_id).first()

        return true_count or 0, false_count or 0

    @classmethod
    def get_error_count_by_device(cls, device_id):
        """
        Get the count of errors (is_error == True) for the specified device_id.

        Args:
        - device_id (int): The ID of the device.

        Returns:
        - int: The count of errors.
        """
        error_count = db.session.query(func.count()).filter(cls.is_error == True, cls.device_id == device_id).scalar()

        return error_count or 0


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()