from marshmallow import Schema, fields

class ZoneSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    # subzones = fields.Nested('SubZoneSchema', many=True)

class SubZoneSchema(Schema):
    class Meta:
        ordered = True
    
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    zone_id = fields.Integer(required=True)
    # devices = fields.Nested('DeviceSchema', many=True)

class DeviceSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    status = fields.Boolean(required=True)
    endpoint = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    subzone_id = fields.Integer(required=True)    

class DeviceStateSchema(Schema):
    class Meta:
        ordered = True

    status = fields.Boolean(required=True)
    is_error = fields.Boolean(required=True)
    updated_at = fields.DateTime(dump_only=True)