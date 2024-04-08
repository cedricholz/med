#!/bin/bash

if ! hash aws 2>/dev/null
then
  yum install -y unzip
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
fi


# Get the keys from SSM and store them as environment variables
DREAMSHIP_API_KEY=$(aws ssm get-parameter --name /DREAMSHIP_API_KEY --with-decryption --region us-west-1 --query Parameter.Value --output text)
echo "export DREAMSHIP_API_KEY=$DREAMSHIP_API_KEY" >> /opt/elasticbeanstalk/deployment/env
SECRET_KEY=$(aws ssm get-parameter --name /SECRET_KEY --with-decryption --region us-west-1 --query Parameter.Value --output text)
echo "export SECRET_KEY=$SECRET_KEY" >> /opt/elasticbeanstalk/deployment/env
SENDGRID_API_KEY=$(aws ssm get-parameter --name /SENDGRID_API_KEY --with-decryption --region us-west-1 --query Parameter.Value --output text)
echo "export SENDGRID_API_KEY=$SENDGRID_API_KEY" >> /opt/elasticbeanstalk/deployment/env
STRIPE_PROD_PUBLISHABLE_KEY=$(aws ssm get-parameter --name /STRIPE_PROD_PUBLISHABLE_KEY --with-decryption --region us-west-1 --query Parameter.Value --output text)
echo "export STRIPE_PROD_PUBLISHABLE_KEY=$STRIPE_PROD_PUBLISHABLE_KEY" >> /opt/elasticbeanstalk/deployment/env
STRIPE_PROD_SECRET_KEY=$(aws ssm get-parameter --name /STRIPE_PROD_SECRET_KEY --with-decryption --region us-west-1 --query Parameter.Value --output text)
echo "export STRIPE_PROD_SECRET_KEY=$STRIPE_PROD_SECRET_KEY" >> /opt/elasticbeanstalk/deployment/env

. /opt/elasticbeanstalk/deployment/env

source $PYTHONPATH/activate

sudo chown -R ec2-user:ec2-user .
source /var/app/venv/*/bin/activate
export $(sudo cat /opt/elasticbeanstalk/deployment/env | xargs)
python manage.py collectstatic --noinput
python manage.py migrate --noinput





