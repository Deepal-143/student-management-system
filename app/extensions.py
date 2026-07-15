"""
Flask extension instances, created here (uninitialized) to avoid circular imports.

Pattern:
  1. Extensions are instantiated here with no app attached yet.
  2. Models and routes import them from this file directly.
  3. The app factory (app/__init__.py) calls db.init_app(app) etc. later,
     attaching these extensions to the actual Flask app instance.

This three-step split is what lets models.py import `db` while app/__init__.py
also imports models - without either file needing to import the other first.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# ORM instance - used by every model to define tables and query data.
db = SQLAlchemy()

# Handles user session logic: who is logged in, protecting routes, etc.
login_manager = LoginManager()

# Handles versioned database schema changes (Alembic under the hood).
migrate = Migrate()

# Where Flask-Login redirects users who try to access a protected page
# without being logged in. 'auth.login' refers to the login view function
# inside the auth Blueprint (built in Phase 4).
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"
