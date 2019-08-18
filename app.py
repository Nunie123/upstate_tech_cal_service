from flask import Flask, jsonify, request
from flask_cors import CORS
import simplejson as json
from configparser import ConfigParser
import requests
import datetime
import pytz
from dateutil.parser import parse


# import config file to global object
config = ConfigParser()
config_file = 'config.ini'
config.read(config_file)

# instantiate flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = config.get('flask', 'secret_key')


# Queries openupstate API for list of groups. Returns dictionary with each source as key (e.g. 'Meetup', 'Eventbrite')
def get_group_lists():
    url = 'https://data.openupstate.org/rest/organizations?org_status=active&_format=json'
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Could not connect to OpenUpstate API at {}.  Status Code: {}'.format(url, r.status_code))
    data = json.loads(r.text)
    all_sources = [x["field_event_service"] for x in data]
    all_sources = list(set(all_sources))    # removes duplicates
    groups_by_source = {}
    for source in all_sources:
        groups_by_source[source] = [i for i in data if i['field_event_service'] == source]
    return groups_by_source


# Takes list of groups and makes API call to Meetup.com to get event details. Returns list.
def get_meetup_events(group_list):
    group_ids = [i['field_events_api_key'] for i in group_list]
    group_ids_str = ','.join(str(group_id) for group_id in group_ids)
    api_key = config.get('meetup', 'api_key')
    url = 'https://api.meetup.com/2/events?key={key}&group_id={ids}'.format(key=api_key, ids=group_ids_str)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Could not connect to Meetup API at {}.  Status Code: {}'.format(url, r.status_code))
    data = json.loads(r.text)
    return data['results']


# Takes list of events from Meetup and returns formatted list of events
def format_meetup_events(events_raw, group_list):
    events = []
    for event in events_raw:
        venue_dict = event.get('venue')
        group_item = [i for i in group_list if i.get('field_events_api_key') == str(event['group']['id'])][0]
        tags = group_item.get('field_org_tags')
        uuid = group_item.get('uuid')
        nid = group_item.get('nid')

        if venue_dict:
            venue = {
                'name': venue_dict.get('name'),
                'address': venue_dict.get('address_1'),
                'city': venue_dict.get('city'),
                'state': venue_dict.get('state'),
                'zip': venue_dict.get('zip'),
                'country': venue_dict.get('country'),
                'lat': venue_dict.get('lat'),
                'lon': venue_dict.get('lon')
            }
        else:
            venue = None
        if event.get('description'):
            description = event.get('description').replace('<p>', '').replace('</p>', '')
        else:
            description = None

        event_dict = {
            'event_name': event.get('name'),
            'group_name': event.get('group').get('name'),
            'venue': venue,
            'url': event.get('event_url'),
            # note: time is converted from unix timestamp to ISO 8601 timestamp.
            # This currently works when both the meeting time and local computer time are in same timezone (US/Eastern).
            # Unsure if it will work when they are in different timezones.
            'time': datetime.datetime.utcfromtimestamp(int(event.get('time'))/1000).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'tags': tags,
            'rsvp_count': event.get('yes_rsvp_count'),
            'created_at': datetime.datetime.utcfromtimestamp(int(event.get('created'))/1000)
                                  .strftime('%Y-%m-%dT%H:%M:%SZ'),
            'description': description,
            'uuid': uuid,
            'nid': nid,
            'data_as_of': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        events.append(event_dict)
    return events


# Takes list of groups hosted on EventBrite and returns list of events.
def get_eventbrite_events(group_list):
    group_ids = [i['field_events_api_key'] for i in group_list if i['field_events_api_key'] != '']
    token = config.get('eventbrite', 'token')
    events = []
    for group_id in group_ids:
        url = 'https://www.eventbriteapi.com/v3/organizers/{}/events/'.format(group_id)
        r = requests.get(url, headers={"Authorization": "Bearer {}".format(token)}, verify=True)
        if r.status_code != 200:
            raise Exception('Could not connect to Eventbrite API at {}.  Status Code: {}'.format(url, r.status_code))
        data = json.loads(r.text)
        if data.get('events'):
            events_list = data.get('events')
            events += events_list
    return events


# Takes list of events hosted on EventBrite and returns list of unique venue dictionaries.
def get_eventbrite_venues(events_list):
    venue_ids = []
    token = config.get('eventbrite', 'token')
    for event in events_list:
        venue_ids.append(event['venue_id'])
    venue_ids = list(set(venue_ids))
    venues = []
    for venue_id in venue_ids:
        if venue_id != None:  # Catch exception if venue id not properly supplied
            url = 'https://www.eventbriteapi.com/v3/venues/{}/'.format(venue_id)
            r = requests.get(url, headers={"Authorization": "Bearer {}".format(token)}, verify=True)
            if r.status_code != 200:
                raise Exception('Could not connect to Eventbrite API at {}.  Status Code: {}'.format(url, r.status_code))
            data = json.loads(r.text)
            venues.append(data)
    return venues


# Takes list of events hosted on EventBrite, list of venues, and list of all groups and returns formatted list of events
def format_eventbrite_events(events_list, venues_list, group_list):
    venues = {}
    events = []
    for venue in venues_list:
        venue_id = venue.get('id')
        venue_address = venue.get('address')
        venue_dict = {}
        if venue_address:
            venue_dict = {
                'name': venue.get('name'),
                'address': '{}, {}'.format(venue_address.get('address_1'), venue_address.get('address_2')),
                'city': venue_address.get('city'),
                'state': venue_address.get('state'),
                'zip': venue_address.get('postal_code'),
                'country': venue_address.get('country'),
                'lat': venue_address.get('latitude'),
                'lon': venue_address.get('longitude')
            }
        venues[venue_id] = venue_dict

    for event in events_list:
        if type(event.get('venue_id')) == str:  # If venue id error
            group_item = [i for i in group_list if i['field_events_api_key'] == event.get('organizer_id')][0]
            group_name = group_item.get('title')
            tags = group_item.get('field_org_tags')
            uuid = group_item.get('uuid')
            nid = group_item.get('nid')
            event_dict = {
                'event_name': event.get('name').get('text'),
                'group_name': group_name,
                'venue': venues[event.get('venue_id')],
                'url': event.get('url'),
                'time': event.get('start').get("utc"),
                'tags': tags,
                'rsvp_count': None,
                'created_at': event.get('created'),
                'description': event.get('description').get('text'),
                'uuid': uuid,
                'nid': nid,
                'data_as_of': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            events.append(event_dict)
    return events


def parse_date(d):
    if isinstance(d, datetime.datetime):
        parsed_date = d
    elif isinstance(d, str):
        try:
            eastern = pytz.timezone('US/Eastern')
            date_no_tz = parse(d)
            parsed_date = eastern.localize(date_no_tz, is_dst=None)
        except ValueError:
            return 'Start date {} is in unknown format. '.format(d)
    else:
        return 'Start date {} is in unknown format. '.format(d)
    return parsed_date


# Takes list of events and returns list of events occuring in specified date range
def filter_events_by_date(events, start_date_str=datetime.datetime.now(datetime.timezone.utc), end_date_str=None):

    if start_date_str:
        start_date = parse_date(start_date_str) - datetime.timedelta(days=1)
    else:
        start_date = None
    end_date = parse_date(end_date_str) if end_date_str else None

    if isinstance(start_date, str) or isinstance(end_date, str):
        return '{}{}'.format(start_date, end_date).replace('None', '')

    if start_date and end_date:
        return [event for event in events if start_date <= parse(event['time']) <= end_date]
    elif start_date:
        return [event for event in events if parse(event['time']) >= start_date]
    elif end_date:
        return [event for event in events if parse(event['time']) <= end_date]
    else:
        return events


# Takes list of events and string of tags to return list of events with specified tags
def filter_events_by_tag(events, tags):
    if tags:
        tags_list = tags.replace(' ', '').split(',')
        print(tags_list)
        filtered_events = []
        for tag in tags_list:
            filtered_events += [event for event in events if tag in event['tags']]
        print(filtered_events)
        return filtered_events
    else:
        return events


@app.route('/api/gtc', methods=['GET', 'POST'])
def get_dates():
    print(request.args)
    start_date = request.args.get('start_date', datetime.datetime.now(datetime.timezone.utc))
    end_date = request.args.get('end_date', None)
    tags = request.args.get('tags', None)
    with open('all_meetings.json') as json_data:
        events_json = json.load(json_data)
        events_date_filter = filter_events_by_date(start_date_str=start_date, end_date_str=end_date, events=events_json)
        events = filter_events_by_tag(events_date_filter, tags)
        return jsonify(events)


if __name__ == '__main__':
    app.run(debug=True)
