import json
import os
import time
from fabric.api import task, local

DOCKER_REPOSITORY = "jelis/cam_server"
TEST_CONTAINER_NAME = "cam_server"


@task
def build():
    local('docker build -t {} .'.format(DOCKER_REPOSITORY))


@task
def run():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    twitter_creds_file = os.path.join(current_dir, "twitter_credentials.json")
    with open(twitter_creds_file, "r") as f:
        creds_json = json.loads(f.read())

    docker_run_cmd = ('docker run -d '
                      '-e TWITTER_CONSUMER_KEY={} '
                      '-e TWITTER_CONSUMER_SECRET={} '
                      '-e TWITTER_ACCESS_TOKEN_KEY={} '
                      '-e TWITTER_ACCESS_TOKEN_SECRET={} '
                      '-p 8080:8080 --name={} {}')

    docker_run_cmd = docker_run_cmd.format(
        creds_json['consumer_key'],
        creds_json['consumer_secret'],
        creds_json['access_token_key'],
        creds_json['access_token_secret'],
        TEST_CONTAINER_NAME,
        DOCKER_REPOSITORY)

    local(docker_run_cmd)


@task
def stop(remove_container=True):
    container_id = local('docker ps --filter "name={}" -aq'.format(TEST_CONTAINER_NAME), capture=True)
    local('docker stop {}'.format(container_id))
    if remove_container:
        local('docker rm {}'.format(container_id))
    return container_id


@task
def test():
    run()
    errors = False
    try:
        time.sleep(1)  # ghetto wait for container
        local('nosetests tests/')
    except:
        errors = True
        raise
    finally:
        its_ok_to_remove_container = not errors
        container_id = stop(its_ok_to_remove_container)
        if errors:
            local('docker logs {}'.format(container_id))
