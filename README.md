# security-cam
* A home security camera management system.
* Receive image data through API POST endpoint and store images in twitter through twitter API.

Running With Docker
==================
* repository = https://hub.docker.com/r/jelis/cam_server/
* docker run -d -p 8080:80 -e TWITTER_CONSUMER_KEY=A -e TWITTER_CONSUMER_SECRET=B -e TWITTER_ACCESS_TOKEN_KEY=C -e TWITTER_ACCESS_TOKEN_SECRET=D -e CLIENT_KEY=E -e CLIENT_SECRET=F jelis/cam_server
