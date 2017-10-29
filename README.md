## Greenville Tech Calendar Service


This application provides an endpoint that will return event data for all groups listed
at https://data.openupstate.org/organizations that host their meeting information on meetup.com
or eventbrite.com.  To be added added or provide updates to this list, make a comment on the github page here: https://github.com/codeforgreenville/OpenData/issues/18

Meeting hosts currently not supported: Facebook, Nvite, Open Collective, and custom websites.

The exposed JSON includes past and future meetings, as made available by the associated event hosting website APIs.  The data is somewhat large (500+
  KB), and the endpoint does not currently provide any method for filtering the data returned.

This application saves the data locally and then exposes the locally saved file.  This prevents excessive API calls to the event hosting websites and improves performance.  Once deployed to a public site, the intention is to have the data updated by a cron job on an hourly basis.

The format of the JSON that returns is:

  `[{
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
