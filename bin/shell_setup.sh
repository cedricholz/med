source /var/app/venv/staging-LQM1lest/bin/activate
export $(sudo cat /opt/elasticbeanstalk/deployment/env | xargs)
cd /var/app/current
python manage.py shell_plus