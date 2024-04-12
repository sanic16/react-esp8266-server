from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS 
from config import Config
from extensions import db, jwt

from resources.user import (UserListResource)

from resources.token import TokenResource, RefreshResource, RevokeResource

from resources.esp8266 import (ZoneListResource, ZoneResource, SubZoneListResource, SubZoneResource,
                               DeviceListResource, DeviceResource, DeviceStatusCountResource)

from models.token import TokenBlocklist

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.init_app(app=app)
    jwt.init_app(app=app)
    cors = CORS(app=app, resources={r"/*": {"origins": "*"}})
    migrate = Migrate(app=app, db=db)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload['jti']
        token = TokenBlocklist.query.filter_by(jti=jti).scalar()

        return token is not None


def register_resources(app):
    api = Api(app=app)
   
    api.add_resource(UserListResource, '/api/users')

    api.add_resource(TokenResource, '/api/token')
    api.add_resource(RefreshResource, '/api/refresh')
    api.add_resource(RevokeResource, '/api/revoke')

    api.add_resource(ZoneListResource, '/api/zones')
    api.add_resource(ZoneResource, '/api/zones/<int:zone_id>')

    api.add_resource(SubZoneListResource, '/api/subzones')
    api.add_resource(SubZoneResource, '/api/subzones/<int:subzone_id>')

    api.add_resource(DeviceListResource, '/api/devices')
    api.add_resource(DeviceResource, '/api/devices/<int:device_id>')

    api.add_resource(DeviceStatusCountResource, '/api/devices/status/count/<int:device_id>')

app = create_app()

if __name__ == '__main__':
    app.run(port=os.environ.get('PORT') or 5000)
