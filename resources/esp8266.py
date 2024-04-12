from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.device import Zone, SubZone, Device, DeviceStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.esp8266 import ZoneSchema, SubZoneSchema, DeviceSchema, DeviceStateSchema
from marshmallow import ValidationError

zone_schema = ZoneSchema()
subZone_schema = SubZoneSchema()
device_schema = DeviceSchema()
device_state_schema = DeviceStateSchema()

class ZoneListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        zones = Zone.get_all(user_id=current_user)
        return zone_schema.dump(zones, many=True), HTTPStatus.OK

    
    @jwt_required()
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()
        
        try:
            data = zone_schema.load(data=json_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages}, HTTPStatus.BAD_REQUEST

        zone = Zone(**data)
        zone.user_id = current_user
        zone.save()

        return zone_schema.dump(zone), HTTPStatus.CREATED

class ZoneResource(Resource):
    @jwt_required()
    def get(self, zone_id):
        zone = Zone.get_by_id(zone_id=zone_id)

        if zone is None:
            return {'message': 'Zone not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != zone.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        return zone_schema.dump(zone), HTTPStatus.OK
    
    @jwt_required()
    def put(self, zone_id):
        zone = Zone.get_by_id(zone_id=zone_id)

        if zone is None:
            return {'message': 'Zone not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != zone.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        json_data = request.get_json()

        try:
            data = zone_schema.load(data=json_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages}, HTTPStatus.BAD_REQUEST

        zone.name = data.get('name')
        zone.save()

        return zone_schema.dump(zone), HTTPStatus.OK

    @jwt_required()
    def delete(self, zone_id):
        zone = Zone.get_by_id(zone_id=zone_id)

        if zone is None:
            return {'message': 'Zone not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != zone.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        zone.delete()
        
        return {}, HTTPStatus.NO_CONTENT
    
#######################################################################################################3

class SubZoneListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        subZones = SubZone.get_all(user_id= current_user)
        return subZone_schema.dump(subZones, many=True), HTTPStatus.OK

    
    @jwt_required()
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()
        
        try:
            data = subZone_schema.load(data=json_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages}, HTTPStatus.BAD_REQUEST

        subZone = SubZone(**data)
        subZone.user_id = current_user
        subZone.save()

        return subZone_schema.dump(subZone), HTTPStatus.CREATED

class SubZoneResource(Resource):
    @jwt_required()
    def get(self, subzone_id):
        subZone = SubZone.get_by_id(subzone_id=subzone_id)

        if subZone is None:
            return {'message': 'subZone not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != subZone.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        return subZone_schema.dump(subZone), HTTPStatus.OK
    
    @jwt_required()
    def put(self, subzone_id):
        subZone = SubZone.get_by_id(subzone_id=subzone_id)

        if subZone is None:
            return {'message': 'subZone not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != subZone.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        json_data = request.get_json()

        try:
            data = subZone_schema.load(data=json_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages}, HTTPStatus.BAD_REQUEST

        subZone.name = data.get('name')
        subZone.save()

        return subZone_schema.dump(subZone), HTTPStatus.OK

    @jwt_required()
    def delete(self, subzone_id):
        subZone = SubZone.get_by_id(subzone_id=subzone_id)

        if subZone is None:
            return {'message': 'subZone not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != subZone.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        subZone.delete()
        
        return {}, HTTPStatus.NO_CONTENT
    
#######################################################################################################

class DeviceListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        devices = Device.get_all(user_id= current_user)
        return device_schema.dump(devices, many=True), HTTPStatus.OK

    
    @jwt_required()
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()
        
        try:
            data = device_schema.load(data=json_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages}, HTTPStatus.BAD_REQUEST

        device = Device(**data)
        device.user_id = current_user
        device.save()

        return device_schema.dump(device), HTTPStatus.CREATED

class DeviceResource(Resource):
    @jwt_required()
    def get(self, device_id):
        device = Device.get_by_id(device_id=device_id)

        if device is None:
            return {'message': 'device not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != device.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        return device_schema.dump(device), HTTPStatus.OK
    
    @jwt_required()
    def put(self, device_id):
        device = Device.get_by_id(device_id=device_id)

        if device is None:
            return {'message': 'device not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != device.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        json_data = request.get_json()

        try:
            data = device_schema.load(data=json_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages}, HTTPStatus.BAD_REQUEST

        device.name = data.get('name')
        device.save()

        return device_schema.dump(device), HTTPStatus.OK

    @jwt_required()
    def delete(self, device_id):
        device = Device.get_by_id(device_id= device_id)

        if device is None:
            return {'message': 'device not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != device.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        device.delete()
        
        return {}, HTTPStatus.NO_CONTENT
    
    @jwt_required()
    def post(self, device_id):
        json_data = request.get_json()

        device = Device.get_by_id(device_id=device_id)

        if device is None:
            return {'message': 'device not found'}, HTTPStatus.NOT_FOUND
        
        try:
            data = device_state_schema.load(data=json_data)
        except ValidationError as error:
            return {'message': 'Validation errors', 'errors': error.messages}, HTTPStatus.BAD_REQUEST

        current_user = get_jwt_identity()

        if current_user != device.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
                
        device_status = DeviceStatus(**data)
        device_status.device_id = device_id
        device_status.save()

        return device_state_schema.dump(device_status), HTTPStatus.CREATED

#######################################################################################################

class DeviceStatusCountResource(Resource):
    @jwt_required()
    def get(self, device_id):
        device = Device.get_by_id(device_id=device_id)

        if device is None:
            return {'message': 'device not found'}, HTTPStatus.NOT_FOUND
        
        current_user = get_jwt_identity()

        if current_user != device.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        
        true_count, false_count = DeviceStatus.get_status_counts_by_device(device_id=device_id)
        total = true_count + false_count
        return {'true_count': float(true_count), 'false_count': float(false_count), 'total': float(total)}, HTTPStatus.OK
    
#######################################################################################################
        
        








