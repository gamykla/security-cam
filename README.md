# security-cam
* A home security camera management system.
* Receive image data through API POST endpoint and store images in twitter through twitter API.

Running With Docker
==================
* repository = https://hub.docker.com/r/jelis/cam_server/
* docker run -d -e TWITTER_CONSUMER_KEY=a -e TWITTER_CONSUMER_SECRET=b -e TWITTER_ACCESS_TOKEN_KEY=c -e TWITTER_ACCESS_TOKEN_SECRET=d jelis/cam_server

Notes
=====
- curl -v -X POST -d '{"a": 1}' -H 'Content-Type: application/json' localhost:8080/captures/
- docker build -t security_cam .


