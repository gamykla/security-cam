FROM python:2.7.12

ADD requirements requirements
RUN pip install -r requirements/base.txt

ADD security_cam security_cam

EXPOSE 80

ADD bin/camserver.sh /camserver.sh
ADD bin/docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/camserver.sh"]