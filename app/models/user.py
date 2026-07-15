"""
User model - represents an admin account that can log into the system.

We use Werkzeug's password hashing (never store plain-text passwords) and
Flask-Login's UserMixin (gives us is_authenticated, is_active, get_id, etc.
for free, so Flask-Login can manage sessions without extra boilerplate).
"""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    """
    Represents an admin user who can log in to manage students.

    Inherits from:
        UserMixin: Adds properties/methods Flask-Login requires
                   (is_authenticated, is_active, is_anonymous, get_id()).
        db.Model:  Marks this class as a SQLAlchemy table.
    """

    # Explicit table name. Without this, SQLAlchemy would auto-generate
    # "user", which works too - but being explicit avoids surprises later
    # (e.g. if "user" clashes with a reserved word in some databases).
    __tablename__ = "users"

    # Primary key: unique identifier for each row, auto-incremented by
    # the database. Every model needs exactly one primary key.
    id = db.Column(db.Integer, primary_key=True)

    # unique=True: the database rejects a second row with the same username.
    # nullable=False: this field is required, can never be empty.
    # index=True: speeds up lookups by username (used on every login attempt).
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)

    # We NEVER store the raw password. We store its hash. String(255) gives
    # enough room for the hash algorithm's output plus its salt/metadata.
    password_hash = db.Column(db.String(255), nullable=False)

    # Records when the admin account was created - useful for auditing.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        """
        Hash the given plain-text password and store the hash.

        Called once when creating the admin account (e.g. via a CLI seed
        script) - never called during normal login.
        """
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """
        Verify a plain-text password against the stored hash.

        Returns True if it matches, False otherwise. Used during login -
        we never decrypt the hash, we hash the attempt and compare hashes.
        """
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        """
        Developer-friendly string shown when printing a User object
        (e.g. in a Python shell or debug logs). Never include the
        password hash here, even though it's already hashed - no reason
        to expose it in logs.
        """
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login calls this automatically on every request to reload the
    logged-in user's object from the ID stored in their session cookie.

    Args:
        user_id (str): the user ID from the session (Flask-Login always
            passes this as a string, even though our primary key is an int).

    Returns:
        User | None: the matching User row, or None if it doesn't exist
        (e.g. the account was deleted after the session cookie was issued).
    """
    return User.query.get(int(user_id))
