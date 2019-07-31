1. SSH into a Linux machine
2. Execute the following commands:
   1. `sudo useradd eventapi -s /bin/bash && passwd eventapi`
   2. `sudo mkdir /home/eventapi/public_html && chown -Rf eventapi:eventapi /home/eventapi/public_html`
   3. `sudo update yum`
   4. `sudo yum install git`
   5. `git clone https://github.com/codeforgreenville/upstate_tech_cal_service.git`
   6. `cd upstate_tech_cal_service`
   7. `curl https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh`
   8. `sh miniconda.sh -b -p $HOME/miniconda`
   9. `export PATH="$HOME/miniconda/bin:$PATH"`
   10. `conda env create -f environment.yml`
   11. `source activate cal_service` OR `conda activate cal_service`
3. Create a local config file, if one does not exist.
   1. `cp config.ini.example config.ini && nano config.ini`
   2. `nano config.ini`
      1. Register your own Eventbrite token https://www.eventbrite.com/support/articles/en_US/How_To/how-to-locate-your-eventbrite-api-user-key?lg=en_US
       2. Register your own a Meetup.com API key https://secure.meetup.com/meetup_api/key/
       3. Flask secret can be any long random string
4. Optionally - Test with gunicorn WSGI Server on a localhost port
   1. `gunicorn --bind 0.0.0.0:8000 app:app`
   2. `wget http://localhost:8000`
5. Optionally - Configure hosting via a Web Server 
   1. Setup gunicorn as a systemd daemon
   2. Configure an Nginx or Apache to "talk" to the gunicorn proxy
