from marshmallow import Schema, fields
from utils import hash_password

class UserSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.Method(required=True, deserialize='load_password')
    is_active = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def load_password(self, value):
        return hash_password(value)
    
   