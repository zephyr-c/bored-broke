from pprint import pformat
import os

from jinja2 import StrictUndefined

import requests

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Event, UserEvent, Interest, connect_to_db, db

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')

EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

@app.route("/", methods=["POST", "GET"])
def homepage():
    """show landing page"""
    return render_template("landingpage.html")

@app.route("/login", methods=["POST"])
def process_login():
    """Log user in to their account.
    Checks for username in db and checks password correct"""

    # gets form data from HTML form pointed at this route
    username = request.form.get('username')
    password = request.form.get('password')

    profile = User.query.filter(User.username == username).first()

    if not profile or not profile.check_password(password):
        flash("Username or Password Incorrect")
        return redirect("/")
    else:
        session['user_id'] = profile.user_id
        flash(f"Welcome back {profile.fname}!")
        return redirect("/event-search")


@app.route("/logout")
def process_logout():
    """Log user out from account by deleting info from Flask session"""

    # There might be a better way to do this as well. More research needed after
    # basic functionality achieved.
    del session['user_id']

    return redirect("/") # can this be changed to let them stay wherever they are?


@app.route("/register", methods=["GET"])
def registration():
    """show registration form"""
    return render_template('registration.html')


@app.route("/register", methods=['POST'])
def process_registration():
    """save new user data in system"""
    new_info = request.form
    users = User.query.all()
    if (new_info['username'] in [user.username for user in users]
       or new_info['email'] in [user.email for user in users]):
        flash("User Already Exists")
        return redirect('/register')
    else:
        new_user = User(username=new_info['username'],
                        # password=new_info['password'],
                        fname=new_info['fname'],
                        lname=new_info['lname'],
                        email=new_info['email'],
                        phone=new_info['phone'],
                        location=new_info['location'],
                        )
        new_user.set_password(new_info['password'])
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.user_id
        flash("Success!")
        return redirect('/event-search')



@app.route("/user-profile")
def user_profile():
    """show user profile/interests"""
    pass


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
               }


    headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

    response = requests.get(EVENTBRITE_URL + "events/search/",
                            params=payload,
                            headers=headers)

    if response.ok:
        data = response.json()  # This was causing an error outside of this if statement
        # if response is an error code there is nothing to turn into json,
        # must check response okay first.
        events = data['events']

        return render_template("search-results.html",
                                results=events)

    else:
        status = "ERROR"
        sub_data = json.load(open('results.json'))
        events = sub_data['events']

        return render_template("search-results.html",
                                results=events,
                                status=status)

        # return render_template("eventbrite_goofed.html")

    # else:
    #     flash(f"Oops! No Events: {response.headers} {response.reason} {response.text}")
    #     events = []

    # return render_template("search-results.html",
    #                        # data=pformat(data),
    #                        results=events)


@app.route("/save-event", methods=["POST"])
def save_event():
    """Save event to user saved events list

reference user ID from session
get event data from event results
query event table to see if event already saved by other user
if already in DB, use existing entry to create new UserEvent
else add event to Event table, and then create new UserEvent
eventually, add to user saved events page/template. """
    # user = User.query.filter_by(user_id = session['user_id']).first()


    pass



if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
