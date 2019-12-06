"""Helper Functions Will Go Here"""
from flask import Flask, session, jsonify
import requests
import os
import json
from model import *

EVENTBRITE_TOKEN = os.environ.get('EVENTBRITE_TOKEN')

EVENTBRITE_URL = "https://www.eventbriteapi.com/v3/"

POSTMAN = os.environ.get('POSTMAN')

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
        response = requests.request("GET", EVENTBRITE_URL + "events/search/",
                                data=payload,
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
        sub_data = json.load(open('sub_data/sf-sub-evts.json'))
        events = sub_data['events']

    custom_events = compress_evt_list(events)
    markers = [event['marker'] for event in custom_events]
    results = {'status': status, 'events': custom_events, 'markers': markers}

    return results

def mock_event_search(payload):

    status = "TEST" + "\n" + str(payload)
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
        # date, time = e['start']['local'].split("T")
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
                            'coords': {
                            'lat': e['venue']['latitude'],
                            'lng': e['venue']['longitude']},
                            # 'img': e['logo']['url'],
                            })
    return custom_events

def evt_date_sort(events):
    """Group Event Results by Date"""
    date_groups = {}
    for event in events:
        date, time = event['date'].split("T")
        date_groups[date] = date_groups.get(date, [])
        date_groups[date].append(event)

    return date_groups

def postman_search(query):
    url = "https://www.eventbrite.com/api/v3/events/search/"

    querystring = {"price":"free","sort_by":"date","expand":"venue","include_all_series_instances":"false",
                   "categories":"103,110,113,105,104,108,107,102,109,116,106,117,118,119,199"}

    payload = json.dumps(query)

    headers = {
    'Connection': "keep-alive",
    'Origin': "https://www.eventbrite.com",
    'X-CSRFToken': "93f583cc160b11eaa47a97136413c932",
    'X-Requested-With': "XMLHttpRequest",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    'DNT': "1",
    'Content-Type': "application/json",
    'Accept': "*/*",
    'Sec-Fetch-Site': "same-origin",
    'Sec-Fetch-Mode': "cors",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "en-US,en;q=0.9",
    'Cache-Control': "no-cache",
    'Postman-Token': POSTMAN,
    'Host': "www.eventbrite.com",
    'Content-Length': "115",
    'Cookie': "ebEventToTrack=; AS=95574d34-1ac5-40f7-8c3d-3d1f11db930f; AN=; janus=v%3D1%26exp_eb_117880_include_long_events_in_search%3DC; SS=AE3DLHSiutW5-BP4TQK_IRCgfVVZSiWIZw; mgrefby=; G=v%3D2%26i%3De2b9ae50-4a96-468e-aced-2c45a60c4daf%26a%3Dc42%26s%3D7f638d11b861f45f7abca3490df2499622ad0f84; eblang=lo%3Den_US%26la%3Den-us; mgref=typeins; SERVERID=djc19; cm=%5B80141133287%5D; mgref=eafil; mgaff80141133287=ebapi; csrftoken=ef258326163011ea877a9ff5f9e03805; SP=AGQgbbmAcaKlFR78UX4RE0ceCiD-hhTvYSTxCRh9xL4CsXvJENi6hWJ8MtOO1k2OMZNiVNer3YIFv-zxsnuQZrUZ1-DUvD-bVYwT0YMZfkMX8GGD0HqaFxcuDh_8u9qhO1GWfGOYbfaLr2u9bwCauruV4XsUnHnxv2HqmNZ1X5JydcLv5kTABvKigApAN6F2xoZDRyhRFzebwLL6qIqsMlG_h0ZHDAszLcHlKgai40djlyBmKT71USg",
    'cache-control': "no-cache"
    }

    response = requests.request("GET", url, data=payload, params=querystring, headers=headers)

    if response.ok:
            status = "OKAY"
            data = response.json()
            events = data['events']
            with open('sub-evts.json', 'w') as outfile:
                json.dump(data, outfile)

    else:
        status = "SUBSTITUTE RESULTS"
        sub_data = json.load(open('sub_data/sf-sub-evts.json'))
        events = sub_data['events']

    custom_events = compress_evt_list(events)
    markers = [event['marker'] for event in custom_events]
    by_date = evt_date_sort(custom_events)
    results = {'events': custom_events, 'markers': markers, 'sorted': by_date}

    return results

def debug_print(problem):
        print("\n")
        print(problem)
        print("\n")



