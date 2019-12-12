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
    eventbrite_id = db.Column(db.String, unique=True)
    event_name = db.Column(db.String)
    event_url = db.Column(db.String)
    location = db.Column(db.String)
    date = db.Column(db.DateTime) #start time and end time should be in datetime object
    category = db.Column(db.String)
    price = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        """Provide helpful representation when printed!"""
        return f"< {self.event_name} >"

    def to_dict(self):
        return {'event_id': self.event_id,
                'eventbrite_id': self.eventbrite_id,
                'event_name': self.event_name,
                'event_url': self.event_url,
                'location': self.location,
                'date': self.date,
                'category': self.category,
                'description': self.description}


class UserEvent(db.Model):
    """Table to handle relationship of user saving of events"""

    __tablename__ = "user_events"

    ue_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    eventbrite_id = db.Column(db.String, db.ForeignKey('events.eventbrite_id'))
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

class Activity(db.Model):

    __tablename__ = "activity_ideas"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity = db.Column(db.String)
    description = db.Column(db.String)
    img = db.Column(db.String)

###############################################################################
# Helper Functions
def example_data():
    User.query.delete()
    UserEvent.query.delete()
    Event.query.delete()

    citrus = User(username='citrus',
                  fname='Citrus',
                  lname='Froot',
                  email='citrus@orangemail.com',
                  phone='433-909-6889',
                  location='94112',
                  avatar='https://robohash.org/citrus?set=set4')
    citrus.set_password('password')

    tripp = User(username='tkleinhaus1',
                 fname='Tripp',
                 lname='Kleinhaus',
                 email='tkleinhaus1@ask.com',
                 phone='590-430-3503',
                 location='29920',
                 avatar='https://robohash.org/eaarchitectomaxime.bmp?set=set3')
    tripp.set_password('KZQq54Rh')

    sinatra = Event(eventbrite_id='80421329361',
                    event_name='In the Style of Frank Sinatra',
                    event_url='https://www.eventbrite.com/e/in-the-style-of-frank-sinatra-tickets-80421329361?aff=ebapi',
                    date='2019-11-08T19:00:00',
                    category='103',
                    description='Vintage Noise has become synonymous with lush vocals and gentle strings, blending timeless jazz and exotic sounds of bossa nova.',
                    )
    
    save = UserEvent(eventbrite_id='80421329361', user_id=1)

def connect_to_db(app, db_uri="postgresql:///bored_data"):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")

