"""Helper Functions Will Go Here"""
from flask import Flask, session, jsonify
import json
from model import *

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

def compress_events(events):
    """Parse search results and keep only relevant event data"""

    custom_events = {}

    for i in range(len(events)):
        e = events[i]
        custom_events[i] = {'name': e['name']['text'],
                            'eventbrite_id': e['id'],
                            'event_url': e['url'],
                            'date': e['start']['local'],
                            'category': e['category_id'],
                            'description': e['summary'],
                            'location': e['venue'],
                            }
    return jsonify(custom_events)

def compress_evt_list(events):
    """Parse search results and keep only relevant event data"""

    custom_events = []

    for e in events:
        custom_events.append({'name': e['name']['text'],
                            'eventbrite_id': e['id'],
                            'event_url': e['url'],
                            'date': e['start']['local'],
                            'category': e['category_id'],
                            'description': e['summary'],
                            'location': e['venue']['address']['localized_address_display'],
                            'marker': {'name': e['name']['text'], 'coords': {
                            'lat': e['venue']['latitude'],
                            'lng': e['venue']['longitude']}},
                            })
    return custom_events


