from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config.db_connect import Config
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(Config)
# CORS(app, supports_credentials=True, expose_headers=["Authorization"])
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import blog
from app.models import tag
from app.models import introduction
from app.models import body
from app.models import content

from app.routes.agentRoute import agentRoute
from app.routes.blogRoute import blogRoute

app.register_blueprint(agentRoute)
app.register_blueprint(blogRoute)