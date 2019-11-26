import os

from jinja2 import StrictUndefined

import requests
import json
import random

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Event, UserEvent, Interest, connect_to_db, db
from functions import *

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')

EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

HEADERS = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

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
        flash("Username or Password Incorrect")
        return redirect("/")
    else:
        login_success(profile.user_id)
        # session['user_id'] = profile.user_id
        flash(f"Welcome back {profile.fname}!")
        return redirect("/event-search")


@app.route("/logout")
def process_logout():
    """Log user out from account by deleting info from Flask session"""

    # There might be a better way to do this as well. More research needed after
    # basic functionality achieved.
    del session['user']

    return redirect("/") # can this be changed to let them stay wherever they are?


@app.route("/register", methods=["GET"])
def registration():
    """show registration form"""
    return render_template('registration.html')


@app.route("/register", methods=['POST'])
def process_registration():
    """save new user data in system"""
    new_info = request.form
    user_info = dict(db.session.query(User.username, User.email).all())
    if (new_info['username'] in user_info.keys()
       or new_info['email'] in user_info.values()):
        flash("User Already Exists")
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
        # session['user_id'] = new_user.user_id
        flash("Success!")
        return redirect('/')


@app.route("/user-profile-<user_id>")
def user_profile(user_id):
    """show user profile/interests"""
    user = User.query.filter(User.user_id == user_id).one()

    return render_template('user-profile.html', user=user)

@app.route("/saved-events-<user_id>")
def show_saved_events(user_id):
    """show list of user's saved events"""
    saved = UserEvent.query.filter(UserEvent.user_id == user_id).all()

    return render_template('saved-events.html', saved=saved)

@app.route("/saved-events.json", methods=['GET'])
def get_user_events():
    saved_events = UserEvent.query.filter_by(user_id = user_id)
    return jsonify({"saved_events": saved_events})


@app.route("/event-search")
def show_search_form():
    """show event search form"""
    return render_template('event-search.html')


@app.route("/event-results")
def find_events():
    """Search for and display free events from EventBrite"""

# Should API calls be helper functions in a separate file???

    query = request.args.get('query')
    location = request.args.get('location')
    distance = request.args.get('distance')
    measurement = request.args.get('measurement')
    sort = request.args.get('sort')

    distance = distance + measurement

    payload = {'q': query,
               'price': 'free',
               'location.address': location,
               'location.within': distance,
               'sort_by': sort,
               'expand': 'venue',
               }
    retry_count = 0
    while retry_count < 5:
        response = requests.get(EVENTBRITE_URL + "events/search/",
                                params=payload,
                                headers=HEADERS)

        if response.ok:
            status = "OKAY"
            data = response.json()
            events = data['events']
            with open('sub-evts.json', 'w') as outfile:
                json.dump(data, outfile)
            break
        else:
            print(response.status_code)
            print("trying again")
            retry_count += 1
            continue

    if retry_count >= 5:
        status = "ERROR"
        sub_data = json.load(open('sub_data/sf-sub-evts.json'))
        events = sub_data['events']

    custom_events = compress_evt_list(events)

    return render_template("search-results.html",
                            results=custom_events,
                            status=status)

        # return render_template("eventbrite_goofed.html")

    # else:
    #     flash(f"Oops! No Events: {response.headers} {response.reason} {response.text}")
    #     events = []


@app.route("/save-event", methods=["POST"])
def save_event():
    """Save event to user saved events list"""

    eventbrite_id = request.form.get('evtID')

    if not Event.query.filter(Event.eventbrite_id == eventbrite_id).first():
        response = requests.get(EVENTBRITE_URL + "events/" + eventbrite_id,
                                headers=HEADERS)
        data = response.json()
        # print("\n")
        # print(data)
        # print("\n")
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

    return "#"+eventbrite_id

@app.route("/activities.json", methods=["GET"])
def get_random_activity():
    """Return random activity selection from database"""
    suggestion = random.choice(Activity.query.all())
    activity = suggestion.activity
    print(activity)
    description = suggestion.description
    print(description)

    return jsonify({"activity": activity,
                    "description": description})

@app.route("/test.json", methods=["GET"])
def serve_test_results():
    sub_data = json.load(open('sub_data/sf-sub-evts.json'))
    events = sub_data['events']
    custom_events = compress_evt_list(events)
    markers = [event['marker'] for event in custom_events]
    if not session.get('user'):
        user_id = None
    else:
        user_id = session['user']['user_id']
    # print(markers)

    return jsonify(results=custom_events,
                   markers=markers,
                   user_id=user_id)

@app.route("/test")
def show_test_page():
    return render_template("test-page.html")



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
