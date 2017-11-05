from crontab import CronTab
from configparser import ConfigParser

# import config file to global object
config = ConfigParser()
config_file = 'config.ini'
config.read(config_file)

aws_username = config.get('aws', 'username')
file_location = config.get('aws', 'update_cal_location')

cron = CronTab(user=aws_username)
job = cron.new(command='python {}'.format(file_location))
job.minute.every(1)

cron.write()
