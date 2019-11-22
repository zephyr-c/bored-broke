"""File to seed to database"""

from sqlalchemy import func
from model import User
#classes below will be defined/seeded later once basic user functionality is up
# from model import Interest
from model import Activity

from model import connect_to_db, db
from server import app
from datetime import datetime

def load_users():
    """Load local user data into database."""

    # Delete all rows in table to prevent duplicate users if we need to
    # run seed file again.
    User.query.delete()

    for row in open("MOCK_DATA.txt"):
        row = row.rstrip().split("|")
        user_id, username, password, fname, lname, email, phone, location, avatar = row

        user = User(user_id=user_id,
                    username=username,
                    # password=password,
                    fname=fname,
                    lname=lname,
                    email=email,
                    phone=phone,
                    location=location,
                    avatar=avatar)
        user.set_password(password)
        # Add user to session or they won't be stored
        db.session.add(user)
    # Commit to DB or user won't end up there ever
    db.session.commit()

def load_activities():
    """Load activity ideas into database"""
    # Delete rows in table to prevent duplicates if file run again
    Activity.query.delete()

    for row in open("activities.txt"):
        row = row.rstrip().split("|")
        activity, description = row

        activity = Activity(activity=activity,
                            description=description,)

        db.session.add(activity)
    db.session.commit()



def set_val_user_id():
    """Set value for thenext user_id after seeding data"""
# Get the max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

# Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)
    # create tables if they don't exist yet
    db.create_all()

    #Import user data
    load_users()
    set_val_user_id()
    load_activities()