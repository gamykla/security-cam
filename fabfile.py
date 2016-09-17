from fabric.api import task, local

DOCKER_REPOSITORY = "jelis/cam_server"
TEST_CONTAINER_NAME = "cam_server"


@task
def build():
    local('docker build -t {} .'.format(DOCKER_REPOSITORY))


@task
def run():
    local('docker run -d -p 8080:8080 --name={} {}'.format(TEST_CONTAINER_NAME, DOCKER_REPOSITORY))


@task
def stop():
    container_id = local('docker ps --filter "name={}" -aq'.format(TEST_CONTAINER_NAME), capture=True)
    local('docker stop {}'.format(container_id))
    local('docker rm {}'.format(container_id))


@task
def test():
    run()
    try:
        local('nosetests tests/')
    finally:
        stop()
