## Greenville Tech Calendar Service


This application provides an endpoint that will return event data for all groups listed
at https://data.openupstate.org/organizations that host their meeting information on meetup.com
or eventbrite.com.  To be added added or provide updates to this list, make a comment on the github page here: https://github.com/codeforgreenville/OpenData/issues/18

Meeting hosts currently not supported: Facebook, Nvite, Open Collective, and custom websites.

The exposed JSON includes past and future meetings, but defaults to providing only future meetings unless a `start_date` is specified. The data comes from the associated event hosting website APIs and is updated every five minutes.

You can access this data by going here: http://nunes.online/api/gtc

You may also filter the return result by providing a `start_date` and `end_date` like so: http://nunes.online/api/gtc?start_date=2018-01-01&end_date=2018-02-01 (the application currently assumes "US/Eastern" as the timezone when a date filter is provided)

The format of the JSON that returns is:


    [{
      'event_name': 'Tuesday Hack Night',
      'group_name': 'Upstate Hackers',
      'venue': {'name': 'Greenville Open Data HQ',
                'address': '101 N. Main St., 3rd Floor',
                'city': 'Greenville',
                'state': 'SC',
                'zip': '29605',
                'country': 'US',
                'lat': 34.851616,
                'lon': -82.398392}
      'url': 'https://data.openupstate.org/',
      'time': '2017-12-24T15:30:00Z',
      'rsvp_count': 42,
      'created_at': '2017-07-04T10:05:00Z',
      'description': 'Let's meet up and hack everything!',
      'data_as_of': '2017-10-29T18:29:14Z'
    }, ...]`

Note:
* All timestamps are in UTC.  
* Some of the description fields include html markup from the host sites.  This application does not verify that there is nothing malicious in the included markup.
