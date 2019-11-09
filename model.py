"""Models and database functions for Event Finding project."""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#####################################################################

#Model Definitions

class User(db.Model):
    """User of Bored and Broke website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True,
                        )
    username = db.Column(db.String(20),
                        nullable=False,
                        unique=True,
                        )
    password_hash = db.Column(db.String(128),
                        nullable=False,
                        )
    fname = db.Column(db.String(20),)
    lname = db.Column(db.String(30),)
    email = db.Column(db.String(30), nullable=False, unique=True,)
    phone = db.Column(db.String(15),)
    location = db.Column(db.String(50),)
    avatar = db.Column(db.String(100),)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Provide helpful representation when printed!"""
        return f"<User {self.user_id} {self.username}>"


class Event(db.Model):
    """An Event Saved to Database"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    eventbrite_id = db.Column(db.Integer)
    event_name = db.Column(db.String)
    event_URL = db.Column(db.String)
    location = db.Column(db.String)
    date = db.Column(db.DateTime) #start time and end time should be in datetime object
    category = db.Column(db.String)
    price = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        """Provide helpful representation when printed!"""
        return f"< {self.event_name} >"


class UserEvent(db.Model):
    """Table to handle relationship of user saving of events"""

    __tablename__ = "user_events"

    ue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    eventbrite_id = db.Column(db.Integer, db.ForeignKey('events.eventbrite_id'))
    attendance = db.Column(db.String(5))

    user = db.relationship("User", backref=db.backref("user_events"))
    event = db.relationship("Event", backref=db.backref("user_events"))


class Interest(db.Model):
    """User Interests Based on EventBrite Categories Stored as Booleans"""

    __tablename__ = "user_interests"

    record_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    music = db.Column(db.Boolean)
    business = db.Column(db.Boolean)
    food = db.Column(db.Boolean)
    community = db.Column(db.Boolean)
    arts = db.Column(db.Boolean)
    film_media = db.Column(db.Boolean)
    sports_fitness = db.Column(db.Boolean)
    health = db.Column(db.Boolean)
    science_tech = db.Column(db.Boolean)
    travel_outdoor = db.Column(db.Boolean)
    charity_causes = db.Column(db.Boolean)
    spirituality = db.Column(db.Boolean)
    family_education = db.Column(db.Boolean)
    holiday = db.Column(db.Boolean)
    government = db.Column(db.Boolean)
    fashion = db.Column(db.Boolean)
    home_lifestyle = db.Column(db.Boolean)
    auto_boat_air = db.Column(db.Boolean)
    hobbies = db.Column(db.Boolean)
    school_activities = db.Column(db.Boolean)
    other = db.Column(db.Boolean)

# class Activity(db.Model):

#     __tablename__ = "activity_suggestions"

#     pass

###############################################################################
# Helper Functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bored_data'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")

