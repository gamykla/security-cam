import json
import os
import time
from fabric.api import task, local

DOCKER_REPOSITORY = "jelis/cam_server"
TEST_CONTAINER_NAME = "cam_server"


def _get_branch():
    return local('git rev-parse --abbrev-ref HEAD', capture=True)


def _get_image_name():
    return "{}:{}".format(DOCKER_REPOSITORY, _get_branch())


@task
def build():
    local('docker build -t {} .'.format(_get_image_name()))


@task
def push():
    local('docker push {}'.format(_get_image_name()))


@task
def run():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file = os.path.join(current_dir, "secrets.json")
    with open(secrets_file, "r") as f:
        secrets_json = json.loads(f.read())

    env_vars = ' '.join('-e {}={}'.format(key, value) for key, value in secrets_json.iteritems())

    docker_run_cmd = 'docker run -d {} -p 8080:8080 --name={} {}'.format(
        env_vars,
        TEST_CONTAINER_NAME,
        _get_image_name())

    local(docker_run_cmd)


def _rm_container(container_id):
    local('docker rm {}'.format(container_id))


@task
def stop(remove_container=True):
    container_id = local('docker ps --filter "name={}" -aq'.format(TEST_CONTAINER_NAME), capture=True)
    local('docker stop {}'.format(container_id))
    if remove_container:
        _rm_container(container_id)
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
        container_id = stop(False)
        if errors:
            local('docker logs {}'.format(container_id))
        _rm_container(container_id)
