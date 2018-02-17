#!/bin/bash

if [[ -z "$PRAELATUS_PORT" ]]; then
    export PRAELATUS_PORT="8000"
fi

if [[ -z "$PRAELATUS_BIND" ]]; then
    export PRAELATUS_BIND="127.0.0.1"
fi

if [[ -z "$PRAELATUS_WORKER_CONNS" ]]; then
    export PRAELATUS_WORKER_CONNS="1000"
fi

if [[ -z "$PRAELATUS_WORKERS" ]]; then
    export PRAELATUS_WORKERS=$(($(grep -c ^processor /proc/cpuinfo) + 1))
fi

# Names of nodes to start
#   most people will only start one node:
CELERYD_NODES=1

CELERY_BIN="/opt/praelatus/.venv/bin/celery"
CELERY_APP="praelatus"
CELERYD_CHDIR="/opt/praelatus/"
CELERYD_OPTS="--time-limit=300 --concurrency=8"
# %n will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"

CELERYD_USER="celery"
CELERYD_GROUP="celery"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1

${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}


VIRTUALENV="$(readlink -f "$0" | sed s%bin/.*\.sh$%%).venv"
echo "Using virtualenv: $VIRTUALENV"
source $VIRTUALENV/bin/activate

echo "Starting celery worker pool..."
$VIRTUALENV/bin/celery -A praelatus multi start worker -P eventlet -c 1000

echo "Starting Praelatus..."
echo "BIND: $PRAELATUS_BIND"
echo "PORT: $PRAELATUS_PORT"
echo "WORKERS: $PRAELATUS_WORKERS"
echo "WORKER CONNS: $PRAELATUS_WORKER_CONNS"
$VIRTUALENV/bin/gunicorn -b $PRAELATUS_BIND:$PRAELATUS_PORT \
	                       -k gevent \
	                       --worker-connections $PRAELATUS_WORKER_CONNS \
	                       -w $PRAELATUS_WORKERS \
	                       praelatus.wsgi
