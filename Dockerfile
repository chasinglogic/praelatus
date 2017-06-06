FROM python:3

WORKDIR /opt/praelatus
COPY requirements.txt requirements.txt

ENV HTTP_PROXY http://mr91060:robinson17@proxy.kroger.com:3128
ENV HTTPS_PROXY http://mr91060:robinson17@proxy.kroger.com:3128
ENV https_proxy http://mr91060:robinson17@proxy.kroger.com:3128
ENV http_proxy http://mr91060:robinson17@proxy.kroger.com:3128

RUN pip install -r /opt/praelatus/requirements.txt

COPY . .

ENV PYTHONPATH /opt/praelatus

EXPOSE 8000


CMD ["gunicorn", "-k", "gevent", "--config", "/opt/praelatus/docker/gunicorn.conf", "praelatus.app"]
