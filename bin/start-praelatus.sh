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

echo "Starting celery worker pool..."
celery -A praelatus multi start worker -P eventlet -c 1000

echo "Starting Praelatus..."
echo "BIND: $PRAELATUS_BIND"
echo "PORT: $PRAELATUS_PORT"
echo "WORKERS: $PRAELATUS_WORKERS"
echo "WORKER CONNS: $PRAELATUS_WORKER_CONNS"
gunicorn -b $PRAELATUS_BIND:$PRAELATUS_PORT \
	 -k gevent \
	 --worker-connections $PRAELATUS_WORKER_CONNS \
	 -w $PRAELATUS_WORKERS \
	 praelatus.wsgi
