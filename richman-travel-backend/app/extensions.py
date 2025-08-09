# app/extensions.py - Initialize all Flask extensions here
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
cors = CORS(
    supports_credentials=True,
    origins=['http://localhost:5173', 'http://127.0.0.1:5173']
)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
