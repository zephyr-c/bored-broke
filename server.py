from pprint import pformat
import os

import requests

from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Event, UserEvent, Interest, connect_to_db, db

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"

EVENTBRITE_TOKEN = '6KGWWHMNISTJOXRVMSSL'
# os.environ.get('EVENTBRITE_TOKEN')

EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

@app.route("/")
def homepage():
    """show landing page"""
    return render_template("landingpage.html")


@app.route("/registration")
def registration():
    """show registration form"""
    pass

@app.route("/register-user")
def process_registration():
    """save new user data in system"""
    pass


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

# Should API calls be helper functions in a seperate file???

    query = request.args.get('query')
    location = request.args.get('location')
    distance = request.args.get('distance')
    measurement = request.args.get('measurement')
    sort = request.args.get('sort')

    if location and distance and measurement:
        distance = distance + measurement

        payload = {'q' : query,
                    'location.address' : location,
                    'location.within' : distance,
                    'sort_by' : sort,
                    }

        headers = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN}

        response = requests.get(EVENTBRITE_URL + "events/search/",
                                params=payload,
                                headers=headers)
        data = response.json()
        print("\n" * 3)
        print(data)
        print("\n"*3)

        if response.ok:
            events = data['events']

        else:
            flash(f"Oops! No Events: {data['error_description']}")
            events = []

        return render_template("search-results.html",
                                data=pformat(data),
                                results=events)
    else:
        flash("Please provide all the required information!")
        return redirect("/event-search")


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug
    connect_to_db(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
