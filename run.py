"""
Entry point for running the Student Management System locally.

Usage:
    python run.py

For production, this file is NOT used directly - a WSGI server like
Gunicorn will import `create_app()` itself (set up in Phase 9 - Docker).
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True enables auto-reload and detailed error pages.
    # app.config["DEBUG"] is already set correctly by our config classes,
    # so we just pass it through here.
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))
