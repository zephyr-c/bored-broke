"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#####################################################################

#Model Definitions

class User(db.Model):
    """User of Bored and Broke website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(30))
    email = db.Column(db.String(30))
    phone = db.Column(db.String(11))
    location = db.Column(db.String(50))


class Event(db.Model):
    """An Event Saved to Database"""

    __tablename__ = "events"

    pass


class UserEvent(db.Model):
    """Table to handle relationship of user saving of events"""

    __tablename__ = "user_events"

    pass


class Interest(db.Model):
    """User Interests Based on EventBrite Categories Stored as Booleans"""

    __tablename__ = "user_interests"

    pass

class Activity(db.Model):

    __tablename__ = "activity_suggestions"

    pass


