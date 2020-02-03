import os

from jinja2 import StrictUndefined

import requests
import json
import random
import datetime

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Event, UserEvent, Interest, connect_to_db, db
from functions import *

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')

EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

HEADERS = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN,
           'Content-Type':'application/json'}

@app.route("/", methods=["POST", "GET"])
def homepage():
    """show landing page"""
    if session.get('user'):
        return redirect("/event-search")
    else:
        return render_template("landingpage.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user in to their account.
    Checks for username in db and checks password correct"""

    username, password = request.form.values()

    profile = find_by_username(username)

    if not profile or not profile.check_password(password):
        flash("Username or Password Incorrect", "danger")
        return redirect("/")
    else:
        login_success(profile.user_id)
        # session['user_id'] = profile.user_id
        flash(f"Welcome back {profile.fname}!", "success")
        return redirect("/event-search")


@app.route("/logout")
def process_logout():
    """Log user out from account by deleting info from Flask session"""

    del session['user']

    return redirect("/") # can this be changed to let them stay wherever they are?


@app.route("/register", methods=["GET"])
def registration():
    """show user registration form"""
    return render_template('registration.html')


@app.route("/register", methods=['POST'])
def process_registration():
    """save new user data in database"""
    new_info = request.form
    user_info = dict(db.session.query(User.username, User.email).all())
    if (new_info['username'] in user_info.keys()
       or new_info['email'] in user_info.values()):
        flash("User Already Exists", "warning")
        return redirect('/register')
    else:
        new_user = User(username=new_info['username'],
                        fname=new_info['fname'],
                        lname=new_info['lname'],
                        email=new_info['email'],
                        phone=new_info['phone'],
                        location=new_info['location'],
                        avatar=f"https://robohash.org/{new_info['username']}?set=set4",
                        )
        new_user.set_password(new_info['password'])
        db.session.add(new_user)
        db.session.commit()
        flash("Success!", "success")
        return redirect('/')


@app.route("/user-profile-<user_id>")
def user_profile(user_id):
    """show specific user's profile"""
    user = User.query.filter(User.user_id == user_id).one()

    return render_template('user-profile.html', user=user)

@app.route("/saved-events-<user_id>")
def show_saved_events(user_id):
    """show list of user's saved events"""
    today = datetime.datetime.now()
    all_saved = UserEvent.query.filter(UserEvent.user_id == user_id).all()
    show_saved = [event for event in all_saved if event.event.date >= datetime.datetime.now()]

    return render_template('saved-events.html', saved=show_saved)


@app.route("/event-search")
def show_search_form():
    """show event search page"""
    return render_template('react-search.html')

@app.route("/event-search.json")
def search_events():
    """search for free events, return JSON results"""
    what = request.args.get('what')
    where = request.args.get("where")
    when = request.args.get('when', datetime.datetime.now())

    payload = {'q': what,
               'location.address': where,
               'start_date.keyword': when,
               'price': 'free',
               'sort_by': 'date',
               }

    results = postman_search(payload)

    if not session.get('user'):
        user_id = None
    else:
        user_id = session['user']['user_id']

    return jsonify(status=results['status'],
                   results=results['events'],
                   markers=results['markers'],
                   sorted=results['sorted'],
                   user_id=user_id)


@app.route("/save-event", methods=["POST"])
def save_event():
    """Save an event's details to user's saved events list in database"""

    eventbrite_id = request.form.get('evtID')
    print("id: " + eventbrite_id)

    if not Event.query.filter(Event.eventbrite_id == eventbrite_id).first():
        response = requests.get(EVENTBRITE_URL + "events/" + eventbrite_id,
                                headers=HEADERS)
        data = response.json()
        debug_print(data)

        new_event = Event(eventbrite_id=eventbrite_id,
                          event_name=data['name']['text'],
                          event_url=data['url'],
                          date=data["start"]["local"],
                          category=data["category_id"],
                          description=data["summary"],
                          )
        db.session.add(new_event)

    new_save = UserEvent(eventbrite_id=eventbrite_id,
                         user_id=session['user']['user_id'])
    db.session.add(new_save)
    db.session.commit()

    return jsonify(status="success")


@app.route("/saved-events.json", methods=["GET"])
def check_saved():
    """Check if user has already saved a given event"""
    evt_id = request.args.get('evtId')
    user = int(request.args.get('userId'))
    check_save = request.args.get('checkSave', False)
    print(type(check_save))

    if check_save == "true":
        all_saved = set(db.session.query(UserEvent.eventbrite_id, UserEvent.user_id).all())
        status = (evt_id, user) in all_saved

        return jsonify(status=status)


    else:
        today = datetime.datetime.now()
        all_saved = UserEvent.query.filter(UserEvent.user_id == user).all()
        saved = [event.event.to_dict() for event in all_saved if event.event.date >= today]

        return jsonify(saved=saved)


@app.route("/activities")
def show_activities():
    """Display activity generator page"""
    return render_template('activities.html')


@app.route("/activities.json", methods=["GET"])
def get_random_activity():
    """Return random activity selection from database as JSON"""
    suggestion = random.choice(Activity.query.all())
    activity = suggestion.activity
    print(activity)
    description = suggestion.description
    print(description)
    img = suggestion.img

    return jsonify({"activity": activity,
                    "description": description,
                    "img": img})



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
