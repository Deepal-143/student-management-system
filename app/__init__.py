"""
Application factory for the Student Management System.

create_app() builds and returns a fully configured Flask app instance.
Using a factory function (rather than a module-level `app = Flask(...)`)
means we can create multiple independently-configured app instances -
one for running the server, a different one for each test - without
them interfering with each other.
"""

import os
from flask import Flask

from app.config import config_by_name
from app.extensions import db, login_manager, migrate


def create_app(config_name=None):
    """
    Build and configure a Flask application instance.

    Args:
        config_name (str): One of 'development', 'testing', 'production'.
            If not provided, falls back to the FLASK_ENV environment
            variable, and finally to 'development'.

    Returns:
        Flask: a fully configured, ready-to-run Flask app.
    """
    # Determine which configuration to load.
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Attach extensions to this specific app instance.
    # (They were created "empty" in extensions.py to avoid circular imports.)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Ensure the instance/ folder exists (SQLite file lives there).
    os.makedirs(app.instance_path, exist_ok=True)

    # Import models INSIDE create_app (not at the top of this file).
    # This is deliberate: importing here, after db.init_app(app) has run,
    # avoids circular imports (models import `db` from extensions.py,
    # and this file would otherwise need to import models before db
    # exists on the app). Flask-Migrate's `flask db migrate` command also
    # needs these imports to happen so it can detect the tables.
    from app.models.user import User  # noqa: F401
    from app.models.student import Student  # noqa: F401

    # --- Custom CLI commands ---
    # Registered on the app so you can run: flask seed-admin
    # This lets us create the first admin account without ever writing
    # credentials into source code or a script that touches the DB directly.
    @app.cli.command("seed-admin")
    def seed_admin():
        """
        Create a default admin account if one doesn't already exist.

        Usage (from the project root, with FLASK_APP set):
            flask seed-admin
        """
        existing = User.query.filter_by(username="admin").first()
        if existing:
            print("Admin user already exists - skipping.")
            return

        admin = User(username="admin")
        admin.set_password("admin123")  # Change this immediately after first login.
        db.session.add(admin)
        db.session.commit()
        print("Admin user created -> username: admin | password: admin123")
        print("IMPORTANT: change this password after your first login.")

    # --- Blueprint registration happens here in later phases ---
    # Phase 4: from app.routes.auth_routes import auth_bp
    #          app.register_blueprint(auth_bp)
    # (Real routes for auth, dashboard, and students will replace the
    #  temporary test route below.)

    @app.route("/")
    def health_check():
        """
        Temporary route to confirm the app factory, config, and
        extensions are wired together correctly. Will be replaced
        by the real dashboard route in Phase 5.
        """
        return {
            "status": "ok",
            "message": "Student Management System backend is running.",
            "environment": config_name,
        }

    return app
