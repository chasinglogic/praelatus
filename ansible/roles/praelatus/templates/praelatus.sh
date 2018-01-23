#!/bin/bash

if [[ $PRAELATUS_PORT == "" ]]; then
    PRAELATUS_PORT="8080"
fi

cd {{ praelatus_installation_location }}
{% if praelatus_src_installation %}
cd app
{% endif %}

/usr/bin/gunicorn -b 127.0.0.1:$PRAELATUS_PORT \
		  -k gevent \
		  --worker-connections 1000 \
      # sets the number of workers to 2 * number of cpus + 1 as per the
      # recommendation in the gunicorn docs
		  -w $(($(grep -c ^processor /proc/cpuinfo) + 1)) \
		  praelatus.wsgi
