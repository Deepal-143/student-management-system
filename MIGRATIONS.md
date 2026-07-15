# Database Migrations — Setup Steps

Run these from the project root, with your virtual environment activated.
Flask-Migrate needs to know which app to talk to via FLASK_APP.

## 1. Tell Flask which app to use

macOS/Linux:
    export FLASK_APP=run.py

Windows (PowerShell):
    $env:FLASK_APP = "run.py"

## 2. Initialize the migrations folder (one-time only)

    flask db init

This creates the `migrations/` folder with Alembic's config. You only
run this once per project — it's already listed in our structure, so
after running it you'll see files appear inside `migrations/`.

## 3. Generate the first migration

    flask db migrate -m "Create students and users tables"

Flask-Migrate compares your SQLAlchemy models against the (currently
empty) database and writes a migration script describing the tables
it needs to create. Nothing happens to the database yet — this just
generates the plan.

## 4. Apply the migration

    flask db upgrade

This actually runs the migration script against instance/database.db,
creating the `students` and `users` tables.

## 5. Create the first admin account

    flask seed-admin

This runs the CLI command we defined in app/__init__.py, creating a
default admin (username: admin, password: admin123). Change this
password once login is built in Phase 4.

## Going forward

Every time you change a model (add a field, change a constraint, etc.):

    flask db migrate -m "Describe what changed"
    flask db upgrade

Commit the new file that appears under migrations/versions/ to Git —
that file IS the record of your schema change, and lets anyone
(including Docker/Kubernetes deployments) reproduce your schema
by running `flask db upgrade` on a fresh database.
