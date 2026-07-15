"""
Configuration classes for the Student Management System.

Using classes (instead of a single flat set of variables) lets us switch
between development, testing, and production behavior just by choosing
which class the app factory loads - no code changes required.
"""

import os
from dotenv import load_dotenv

# Load variables from the .env file into the process environment.
# This must happen before we read any os.environ values below.
load_dotenv()

# Absolute path to the project root (one level up from this file's folder).
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """
    Base configuration shared by every environment.

    Environment-specific classes below inherit from this and override
    only what needs to change.
    """

    # Secret key signs session cookies and CSRF tokens.
    # Falls back to a default ONLY so the app doesn't crash if .env is
    # missing during initial setup - never rely on this default in production.
    SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-default-key-do-not-use-in-prod")

    # Disables a SQLAlchemy feature we don't use (event tracking on every
    # change) that adds overhead and emits a warning if left enabled.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Max upload size for profile photos: 2 MB. Prevents abuse via huge files.
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    # Folder where uploaded student photos are saved.
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")


class DevelopmentConfig(Config):
    """Used while building and testing the app on your own machine."""

    DEBUG = True

    # SQLite database file stored inside the instance/ folder.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    )


class TestingConfig(Config):
    """Used automatically when running the test suite (Phase 8)."""

    TESTING = True
    DEBUG = True

    # In-memory database: created fresh and destroyed after each test run,
    # so tests never touch or depend on real data.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    # CSRF is disabled in tests only so form-submission tests don't need
    # to simulate CSRF tokens. Never disable this in development/production.
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Used when deployed (e.g. inside Docker / Kubernetes)."""

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'database.db')}"
    )


# Maps the FLASK_ENV string value to the matching config class,
# so the app factory can do: config_by_name[os.environ["FLASK_ENV"]]
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
