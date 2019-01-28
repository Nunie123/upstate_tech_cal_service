heroku login

heroku create greenville-cal-service (name can be anything, as long as unique to heroku)

git push heroku master

heroku config:set FLASK_KEY=secret

heroku config:set MEETUP_KEY=secret

heroku config:set EVENTBRITE_KEY=secret

SHELL=/bin/bash
0 2 * * * cd /home/ed/dev/upstate_tech_cal_service && source activate cal_service && export FLASK_KEY="secret" && MEETUP_KEY="secret" && EVENTBRITE_KEY="secret" && python update_cal_data.py && git add all_meetings.json && git push https://github.com/Nunie123/upstate_tech_cal_service.git && git push heroku master