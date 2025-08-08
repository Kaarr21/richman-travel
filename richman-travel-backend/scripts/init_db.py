#!/usr/bin/env python3
# scripts/init_db.py - Database initialization script

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db# Flask Backend Code Organization and Fixes

## 1. Fix app/extensions.py (currently named extentions.py)

**File: `app/extensions.py`** (rename from extentions.py)

```python
# app/extensions.py - Initialize all Flask extensions here
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
