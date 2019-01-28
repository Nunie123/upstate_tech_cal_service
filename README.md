## Greenville Tech Meetup Events / Calendar API Service

This application provides an endpoint to return event data for all [meetup groups](https://data.openupstate.org/organizations) listed in the [meetups API](https://github.com/codeforgreenville/OpenData/issues/17) if they host their meetings on [meetup.com](https://github.com/codeforgreenville/upstate_tech_cal_service/issues/2)
or [eventbrite.com](https://github.com/codeforgreenville/upstate_tech_cal_service/issues/4).

Meeting services currently not supported: [Facebook](https://github.com/codeforgreenville/upstate_tech_cal_service/issues/5), [Nvite](https://github.com/codeforgreenville/upstate_tech_cal_service/issues/6), [Open Collective](https://github.com/codeforgreenville/upstate_tech_cal_service/issues/2), and [custom websites](https://github.com/codeforgreenville/upstate_tech_cal_service/issues/7).

To be added or provided updates to this list, make a comment on [one of the issues](https://github.com/codeforgreenville/upstate_tech_cal_service/issues).

The exposed JSON includes past and future meetings, but defaults to providing only future meetings unless a `start_date` is specified. The data comes from the associated event hosting website APIs and is updated every five minutes.

You can access this data by going here: https://greenville-cal-service.herokuapp.com/api/gtc

### Examples
* [HackGreenville.com](https://hackgreenville.com/events)
* [OpenWorks' Dashboard](https://joinopenworks.com/dashboard/meetups.php)


### Documentation
You may filter by any tags applied to the organization on the openupstate.org api.  Currently the openupstate.org api only provides Tag IDs (i.e. an integer) instead of descriptive tags. (e.g. https://greenville-cal-service.herokuapp.com/api/gtc?tags=1)

You may also filter the return result by providing a `start_date` and `end_date` like so: https://greenville-cal-service.herokuapp.com/api/gtc?start_date=2018-01-01&end_date=2018-02-01 (the application currently assumes "US/Eastern" as the timezone when a date filter is provided)

The format of the JSON that returns is:


    [{
      "event_name": "Tuesday Hack Night",
      "group_name": "Upstate Hackers",
      "venue": {"name": "Greenville Open Data HQ",
                "address": "101 N. Main St., 3rd Floor",
                "city": "Greenville",
                "state": "SC",
                "zip": "29605",
                "country": "US",
                "lat": 34.851616,
                "lon": -82.398392}
      "url": "https://data.openupstate.org/",
      "time": "2017-12-24T15:30:00Z",
      "tags": "1"
      "rsvp_count": 42,
      "created_at": "2017-07-04T10:05:00Z",
      "description": "Let"s meet up and hack everything!",
      "data_as_of": "2017-10-29T18:29:14Z"
    }, ...]

Note:
* All timestamps are in UTC.  
* Some of the description fields include html markup from the host sites.  This application does not verify that there is nothing malicious in the included markup.
