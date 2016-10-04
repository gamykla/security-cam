import json
import os
import time
from fabric.api import task, local

DOCKER_REPOSITORY = "jelis/cam_server"
TEST_CONTAINER_NAME = "cam_server"


def _get_branch():
    return local('git rev-parse --abbrev-ref HEAD', capture=True)


def _get_image_name():
    tag = _get_branch()
    if tag == "master":
        tag = "latest"

    return "{}:{}".format(DOCKER_REPOSITORY, tag)


@task
def build():
    local('docker build -t {} .'.format(_get_image_name()))


@task
def push():
    local('docker push {}'.format(_get_image_name()))


def _get_kube_config():
    fq_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(fq_dir, "kubernetes/kubeconfig.json")) as f:
        return json.loads(f.read())


@task
def deploy_service():
    """ Deploy a kubernetes service for the camserver"""
    fq_dir = os.path.dirname(os.path.abspath(__file__))
    config = _get_kube_config()
    kube_config_file = config['kubeConfig']
    descriptors_dir = config['descriptorsLocation']
    fq_descriptors_dir = os.path.join(fq_dir, descriptors_dir)
    fq_kube_config = os.path.join(fq_dir, kube_config_file)

    local('kubectl --kubeconfig={} create -f {}'.format(
        fq_kube_config, os.path.join(fq_descriptors_dir, 'service.yaml')))


@task
def deploy_pods():
    """ deploy kubernetes pods for the cam server"""
    fq_dir = os.path.dirname(os.path.abspath(__file__))
    config = _get_kube_config()
    kube_config_file = config['kubeConfig']
    descriptors_dir = config['descriptorsLocation']

    fq_kube_config = os.path.join(fq_dir, kube_config_file)
    fq_descriptors_dir = os.path.join(fq_dir, descriptors_dir)

    local('kubectl --kubeconfig={} delete deployment camserver'.format(fq_kube_config))
    local('kubectl --kubeconfig={} create -f {}'.format(
        fq_kube_config, os.path.join(fq_descriptors_dir, 'deployment.yaml')))
    local('kubectl --kubeconfig={} get pods'.format(fq_kube_config))


@task
def run():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file = os.path.join(current_dir, "secrets.json")
    with open(secrets_file, "r") as f:
        secrets_json = json.loads(f.read())

    env_vars = ' '.join('-e {}={}'.format(key, value) for key, value in secrets_json.iteritems())

    docker_run_cmd = 'docker run -d {} -p 8080:80 --name={} {}'.format(
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
