from flask import Flask, jsonify
from configparser import ConfigParser
import requests
import simplejson as json



# import config file to global object
config = ConfigParser()
config_file = 'config.ini'
config.read(config_file)

# instantiate flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.get('flask','Secret_key')

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

def get_meetup_meetings():
    meeting_list = get_meeting_list()['Meetup']
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
                'country': event.get('venue').get('localized_country_name'),
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
            'time': event.get('time'),
            'rsvp_count': event.get('yes_rsvp_count'),
            'created_at': event.get('created'),
            'description': description
        }
        events.append(event_dict)
    return events



@app.route('/', methods=['GET'])
def get_dates():
    return jsonify(get_meetup_meetings())


if __name__ == '__main__':
    app.run(debug = True)
