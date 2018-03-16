1. Push local changes to remote repo.
2. SSH into server, cd into `upstate_tech_cal_service` folder.
3. Pull changes from remote repo.
4. Make `update_cal_data.py` executable: `chmod +x update_cal_data.py`
5. Make sure that config.ini is up to date (make edits with nano).
6. Reload daemon: `sudo systemctl daemon-reload`
7. Restart gunicorn: `sudo systemctl restart gunicorn`
8. Restart nginx: `sudo systemctl restart nginx`


Helpful information here: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
