'''
This application provides an endpoint that will return event data for all groups listed
at https://data.openupstate.org/organizations and host their meeting information on meetup.com
or eventbrite.com.
Meeting hosts currently not supported: Facebook, Nvite, Open Collective, and custom websites.
'''


from flask import Flask, jsonify
import simplejson as json
from configparser import ConfigParser
import requests
import datetime




# import config file to global object
config = ConfigParser()
config_file = 'config.ini'
config.read(config_file)

# instantiate flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get('flask','Secret_key')

# Gets list of groups, concatenates meeting lists for all groups, then saves json locally.
def refresh_all_meetings():
    meeting_list = get_meeting_list()
    events = (
        get_meetup_events(meeting_list['Meetup'])
        + get_eventbrite_events(meeting_list['Eventbrite'])
        )
    with open('all_meetings.json', 'w') as outfile:
        json.dump(events, outfile)
    return events


# Queries openupstate API for list of groups describing where they host event info
def get_meeting_list():
    url = 'https://data.openupstate.org/rest/organizations?org_status=active'
    r = requests.get(url)
    data = json.loads(r.text)    # current meeting sources: '', 'Facebook', 'Nvite', 'Eventbrite', 'Meetup', 'Unknown', 'Open Collective'
    all_sources = [x["field_event_service"] for x in data]
    all_sources = list(set(all_sources))
    sorted_sources = {}
    for source in all_sources:
        sorted_sources[source] = [i for i in data if i['field_event_service'] == source and i['field_events_api_key'] != '7709021031'] # this key is for Greer Programmers Group, but is wrong
    return sorted_sources

# Takes list of groups and makes API call to Meetup.com to get event details. Returns list.
def get_meetup_events(meeting_list):
    group_ids = [i['field_events_api_key'] for i in meeting_list]
    group_ids_str = ','.join(str(group_id) for group_id in group_ids)
    api_key = config.get('meetup','api_key')
    url = 'https://api.meetup.com/2/events?key={key}&group_id={ids}'.format(key=api_key, ids=group_ids_str)
    r = requests.get(url)
    data = json.loads(r.text)
    events_raw = data['results']
    events=[]
    for event in events_raw:
        if event.get('venue'):
            venue = {
                'name': event.get('venue').get('name'),
                'address': event.get('venue').get('address_1'),
                'city': event.get('venue').get('city'),
                'state': event.get('venue').get('state'),
                'zip': event.get('venue').get('zip'),
                'country': event.get('venue').get('country'),
                'lat': event.get('venue').get('lat'),
                'lon': event.get('venue').get('lon')
            }
        else: venue = None
        if event.get('description'):
            description = event.get('description').replace('<p>','').replace('</p>','')
        else: description = None
        event_dict = {
            'event_name': event.get('name'),
            'group_name': event.get('group').get('name'),
            'venue': venue,
            'url': event.get('event_url'),
    #note: time is converted from unix timestamp to ISO 8601 timestamp.  This currently works when both the meeting time and local computer time are in same timezone (US/Eastern).  Unsure if it will work when they are in different timezones.
            'time': datetime.datetime.utcfromtimestamp(int(event.get('time'))/1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'rsvp_count': event.get('yes_rsvp_count'),
            'created_at': datetime.datetime.utcfromtimestamp(int(event.get('created'))/1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'description': description,
            'data_as_of': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        events.append(event_dict)
    return events

# Takes list of groups and makes API call to EventBrite to get event details. Returns list.
def get_eventbrite_events(meeting_list):
    group_ids = [i['field_events_api_key'] for i in meeting_list]
    token = config.get('eventbrite','token')
    events=[]
    for group_id in group_ids:
        url = 'https://www.eventbriteapi.com/v3/organizers/{}/events/'.format(group_id)
        r = requests.get(url,headers = {"Authorization": "Bearer {}".format(token)},verify = True)
        data = json.loads(r.text)
        if data.get('events'):
            events_list = data.get('events')
            venue_ids = []
            for event in events_list:
                venue_ids.append(event['venue_id'])
            venue_ids = list(set(venue_ids))
            venues={}
            for venue_id in venue_ids:
                url = 'https://www.eventbriteapi.com/v3/venues/{}/'.format(venue_id)
                r = requests.get(url,headers = {"Authorization": "Bearer {}".format(token)},verify = True)
                data = json.loads(r.text)
                venue = {
                    'name': data.get('name'),
                    'address': '{}, {}'.format(data.get('address').get('address_1'),data.get('address').get('address_2')),
                    'city': data.get('address').get('city'),
                    'state': data.get('address').get('state'),
                    'zip': data.get('address').get('postal_code'),
                    'country': data.get('address').get('country'),
                    'lat': data.get('address').get('latitude'),
                    'lon': data.get('address').get('longitude')
                }
                venues[venue_id] = venue
            group_name = [i['title'] for i in meeting_list if i['field_events_api_key'] == group_id][0]
            for event in events_list:
                event_dict = {
                    'event_name': event.get('name').get('text'),
                    'group_name': group_name,
                    'venue': venues[event.get('venue_id')],
                    'url': event.get('url'),
                    'time': event.get('start').get("utc"),
                    'rsvp_count': None,
                    'created_at': event.get('created'),
                    'description': event.get('description').get('text'),
                    'data_as_of': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
                }
                events.append(event_dict)
    return events




@app.route('/', methods=['GET'])
def get_dates():
    with open('all_meetings.json') as json_data:
        return jsonify(json.load(json_data))


if __name__ == '__main__':
    app.run(debug = True)
