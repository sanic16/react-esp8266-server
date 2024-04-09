from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS 
from config import Config
from extensions import db, jwt
from models.device import Zone

from resources.user import (UserListResource)

from resources.token import TokenResource, RefreshResource, RevokeResource

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

app = create_app()

if __name__ == '__main__':
    app.run(port=os.environ.get('PORT') or 5000)
