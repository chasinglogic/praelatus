FROM python:3

RUN mkdir -p /opt/praelatus
WORKDIR /opt/praelatus

ADD ./requirements.txt /opt/praelatus/requirements.txt
RUN pip install -r requirements.txt
RUN pip install -r requirements.dev.txt

ADD . /opt/praelatus

RUN python manage.py collectstatic

ENTRYPOINT python manage.py runserver