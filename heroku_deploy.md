heroku login

heroku create greenville-cal-service (name can be anything, as long as unique to heroku)

git push heroku master

heroku config:set FLASK_KEY=secret

heroku config:set MEETUP_KEY=secret

heroku config:set EVENTBRITE_KEY=secret
