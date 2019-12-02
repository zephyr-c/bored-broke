"""Helper Functions Will Go Here"""
from flask import Flask, session, jsonify
import requests
import os
import json
from model import *

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')

EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

HEADERS = {'Authorization': 'Bearer ' + EVENTBRITE_TOKEN,
           'Content-Type':'application/json'}

def login_success(user_id):
    """Adds user data to flask session after successful log in/password check"""
    session['user'] = {}
    saved_events = UserEvent.query.filter_by(user_id = user_id).all()
    user = session['user']
    user['user_id'] = user_id
    user['saved'] = [event.eventbrite_id for event in saved_events]

def find_by_username(username):
    """Helper query to search db by username"""
    return User.query.filter(User.username == username).first()

def search_events(payload):
    """Search EventBrite API"""
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
        status = "SUBSTITUTE RESULTS"
        sub_datsa = json.load(open('sub_data/sf-sub-evts.json'))
        events = sub_data['events']

    custom_events = compress_evt_list(events)
    markers = [event['marker'] for event in custom_events]
    results = {'status': status, 'events': custom_events, 'markers': markers}

    return results

def mock_event_search(payload):
    print("\n")
    print(payload)
    print("\n")

    status = "TEST"
    sub_data = json.load(open('sub_data/sf-jazz.json'))
    events = sub_data['events']

    custom_events = compress_evt_list(events)
    markers = [event['marker'] for event in custom_events]
    results = {'status': status, 'events': custom_events, 'markers': markers}

    return results

def compress_evt_list(events):
    """Parse search results and keep only relevant event data"""

    custom_events = []

    for e in events:
        date, time = e['start']['local'].split("T")
        custom_events.append({'name': e['name']['text'],
                            'eventbrite_id': e['id'],
                            'event_url': e['url'],
                            'event_date': {'date': date, 'start_time': time},
                            'category': e['category_id'],
                            'description': e['summary'],
                            'location': e['venue']['address']['localized_address_display'],
                            'marker': {'name': e['name']['text'], 'coords': {
                            'lat': e['venue']['latitude'],
                            'lng': e['venue']['longitude']}},
                            })
    return custom_events

    def evt_date_sort(events):
        """Group Event Results by Date"""
        date_groups = {}
        for event in events:
            date, time = event[date].split("T")
            date_groups[date] = date_groups.get(date, [])
            date_groups[date].append(event)

        return date_groups



