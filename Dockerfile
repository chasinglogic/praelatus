FROM python:3

WORKDIR /opt/praelatus
COPY . .
ENV PYTHONPATH /opt/praelatus
RUN apt-get install libpq-dev
RUN pip install -r /opt/praelatus/requirements.txt

EXPOSE 8000

CMD ["celery", "multi", "start", "-A" "praelatus.events", "&&", "gunicorn", "-k", "gevent", "--reload", "-b", "0.0.0.0:8000", "praelatus.app"]
