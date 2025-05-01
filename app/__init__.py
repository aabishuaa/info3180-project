from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from .config import Config

# Create the Flask application
app = Flask(__name__) 
app.config.from_object(Config)

# Initialize extensions
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app,
     resources={ r"/api/*": {"origins": "http://localhost:5173"} },
     supports_credentials=True)

from app.views import frontend
app.register_blueprint(frontend)

# No need for this line - it creates the circular import
# from app import views