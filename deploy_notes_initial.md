1. Open a Command Prompt / Terminal / Shell, either:
   1. On your local computer / localhost
   1. Or, if you develop on a remote server then SSH into th remote machine.
2. Execute the following commands:
   1. (Optional) For Production or Remote Servers Only
      1. `sudo useradd usernamehere -s /bin/bash && passwd usernamehere`
      2. `sudo mkdir /home/usernamehere/public_html && chown -Rf usernamehere:groupnamehere /home/usernamehere/public_html`
   3. (Optional) Install Git on your operating system, assuming you don't already have it installed:
      1. RedHat / CentOS / Fedora: `sudo update yum` && `sudo yum install git`
      1. Ubuntu / Debian: `sudo apt-get update` && `sudo apt-get install git`
      1. Mac: `sudo brew install git`
   1. `cd` to change the directory to where you want the git repository / application to be downloaded
   5. Clone the GitHub repository
      1. Using the SSH protocol: `git clone git@github.com:codeforgreenville/upstate_tech_cal_service.git`
      1. Or, using the HTTPS protcol: `git clone https://github.com/codeforgreenville/upstate_tech_cal_service.git`
   6. `cd upstate_tech_cal_service`
   7. `curl https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh`
   8. `sh miniconda.sh -b -p $HOME/miniconda`
   9. `export PATH="$HOME/miniconda/bin:$PATH"`
   10. `conda env create -f environment.yml`
   1. Activate the application environment
      1. `conda activate cal_service`
      1. Or, the older way will work too: `source activate cal_service`
3. Create a local config.ini file, if one does not exist.
   1. `cp config.ini.example config.ini && nano config.ini`
   1. Fill in the placeholders, "ABC123", values in your config.ini with the real values for the following, `nano config.ini`
      1. Register your own [Eventbrite token](https://www.eventbrite.com/support/articles/en_US/How_To/how-to-locate-your-eventbrite-api-user-key?lg=en_US)
       2. Register your own a [Meetup.com API key](https://secure.meetup.com/meetup_api/key/)
       3. Flask secret can be any long random string
5. Test with gunicorn WSGI Server on a localhost port
   1. Run the following to generate an up to date all_meetsups.json
   2. cd ~/upstate_tech_cal_service && conda activate cal_service && python update_cal_data.py && conda deactivate
   2. `gunicorn --bind 0.0.0.0:8000 app:app`
   2. `wget http://localhost:8000/api/gtc?tags=1'`
4. (Optional) On Remote or Production Servers - Setup a cronjob to generate the all_meetings.json, for example, at :35 after every hour
   1. `crontab -e -u usernamehere`
   2. `35 * * * * source $HOME/.bashrc; cd ~/upstate_tech_cal_service && conda activate cal_service && python update_cal_data.py && conda deactivate`
6. (Optional) Configure hosting via a real Web Server, like Apache or Nginx
   1. Setup gunicorn as a systemd daemon
   2. Configure an Nginx or Apache to "talk" to the gunicorn via the respective "proxy" directive(s)
