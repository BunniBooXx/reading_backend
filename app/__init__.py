from flask import Flask 
from config import Config
from flask_cors import CORS
from .models import db,User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .auth import auth
from .book import book 
from .user import user



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)


jwt= JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


app.register_blueprint(auth)
app.register_blueprint(book)
app.register_blueprint(user)

