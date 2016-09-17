FROM alpine:3.4

RUN apk add --no-cache python && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
rm -r /root/.cache

ADD requirements requirements
ADD security_cam security_cam
RUN pip install -r requirements/base.txt

EXPOSE 8080

ENTRYPOINT python /security_cam/cam_server.py