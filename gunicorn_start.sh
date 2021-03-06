#!/bin/bash

# As seen in http://tutos.readthedocs.org/en/latest/source/ndg.html

NAME="CMJ"                                     # Name of the application (*)
DJANGODIR=/storage2/django-apps/cmj                     # Django project directory (*)
SOCKFILE=/storage2/django-apps/cmj/run/gunicorn.sock    # we will communicate using this unix socket (*)
USER=djangoapps                                   # the user to run as (*)
GROUP=djangoapps                                  # the group to run as (*)
NUM_WORKERS=4                                   # how many worker processes should Gunicorn spawn (*)
                                                # NUM_WORKERS = 2 * CPUS + 1
DJANGO_SETTINGS_MODULE=cmj.settings            # which settings file should Django use (*)
DJANGO_WSGI_MODULE=cmj.wsgi                    # WSGI module name (*)

echo "Starting $NAME as djangoapps"

# Activate the virtual environment
cd $DJANGODIR
source /storage2/django-apps/.virtualenvs/cmj/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE \
  --timeout 600
