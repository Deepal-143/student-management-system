"""
Student model - the core entity of the Student Management System.
"""

from datetime import datetime

from app.extensions import db


class Student(db.Model):
    """
    Represents a single student record.

    Design notes:
        - `id` is the database's internal primary key (auto-incrementing).
        - `student_id` is the human-facing identifier (e.g. a roll/admission
          number). We keep it separate from `id` because business IDs often
          need to be reassigned, formatted, or reset in ways that would be
          dangerous to do to a primary key used in foreign-key relationships.
    """

    __tablename__ = "students"

    # --- Internal primary key ---
    id = db.Column(db.Integer, primary_key=True)

    # --- Human-facing identifier ---
    # unique=True stops two students from sharing the same roll number.
    # index=True speeds up searches/filtering by this field.
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)

    # --- Core personal details ---
    full_name = db.Column(db.String(100), nullable=False, index=True)

    # unique=True: no two students can register with the same email.
    email = db.Column(db.String(120), unique=True, nullable=False)

    # Stored as a string, not a number - phone numbers can have leading
    # zeros, +country codes, or dashes, none of which survive as integers.
    phone_number = db.Column(db.String(20), nullable=False)

    # --- Academic details ---
    # index=True because "filter by course" is a required feature -
    # an index makes that WHERE clause fast even as the table grows.
    course = db.Column(db.String(100), nullable=False, index=True)

    semester = db.Column(db.Integer, nullable=False, index=True)

    # Float works fine for a value like 8.75. The CheckConstraint below
    # enforces the valid academic range (0.0 - 10.0) at the database level,
    # so bad data can't get in even if a form validation is ever bypassed.
    cgpa = db.Column(db.Float, nullable=False)

    # --- Metadata ---
    # default=datetime.utcnow: automatically set the first time a row is
    # created. We store UTC, not local time, so the data stays consistent
    # regardless of which server timezone eventually runs this in production.
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Optional field: stores just the filename (e.g. "3f8a1c.jpg"), not the
    # full path. The full path is reconstructed in templates via
    # url_for('static', filename='uploads/' + profile_photo). Keeping only
    # the filename in the DB means we can change the storage location
    # (e.g. move to cloud storage later) without touching existing rows.
    profile_photo = db.Column(db.String(255), nullable=True)

    __table_args__ = (
        # Enforces CGPA stays within a valid academic range at the DB level.
        db.CheckConstraint("cgpa >= 0.0 AND cgpa <= 10.0", name="check_cgpa_range"),
        # Enforces semester is a realistic value (adjust upper bound if your
        # program has more/fewer semesters).
        db.CheckConstraint("semester >= 1 AND semester <= 8", name="check_semester_range"),
    )

    def __repr__(self):
        """Developer-friendly representation, useful when debugging in a shell."""
        return f"<Student {self.student_id} - {self.full_name}>"

    def to_dict(self):
        """
        Convert this model instance into a plain dictionary.

        Useful for JSON API responses (e.g. dashboard stats, AJAX search
        results) without manually listing fields in every route.
        """
        return {
            "id": self.id,
            "student_id": self.student_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "course": self.course,
            "semester": self.semester,
            "cgpa": self.cgpa,
            "date_added": self.date_added.strftime("%Y-%m-%d") if self.date_added else None,
            "profile_photo": self.profile_photo,
        }
