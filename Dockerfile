FROM python:2.7.12

ADD requirements requirements
RUN pip install -r requirements/base.txt

ADD security_cam security_cam

EXPOSE 80

ENTRYPOINT gunicorn --bind 0.0.0.0:80 --workers 6 --keep-alive 1 --timeout 30 --worker-class gevent security_cam.wsgi:app