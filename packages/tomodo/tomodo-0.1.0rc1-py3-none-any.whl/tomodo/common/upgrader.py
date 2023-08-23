import logging
from time import sleep
from typing import Dict, List

import docker
from docker.models.containers import Container
from pymongo import MongoClient
from pymongo.errors import AutoReconnect
from rich.console import Console


console = Console()
logger = logging.getLogger("rich")


def get_mongodb_version(host: str):
    mongo_client = MongoClient(host)
    server_version = mongo_client.server_info().get("version")
    return server_version


def list_rs_members(replica_set_host: str):
    mongo_client = MongoClient(replica_set_host)
    rs_status = mongo_client.admin.command("replSetGetStatus")
    return [{"name": m.get("name"), "stateStr": m.get("stateStr")} for m in rs_status.get("members")]


def set_fcv(member_name: str, target_version: str):
    mongo_client = MongoClient(f"mongodb://{member_name}/")
    target_fcv = target_version
    if len(target_version.split(".")) > 2:
        target_fcv = ".".join(target_version.split(".")[:-1])
    mongo_client.admin.command("setFeatureCompatibilityVersion", target_fcv)
    logger.info(f"{member_name} is now configured with FCV {target_fcv}")


def step_down_primary(member_name: str):
    logger.info(f"Stepping down {member_name}")
    mongo_client = MongoClient(f"mongodb://{member_name}/")
    timeout = 5
    try:
        mongo_client.admin.command("replSetStepDown", 10)
    except AutoReconnect:
        pass
    logger.info(f"Sleeping {timeout} seconds")
    sleep(timeout)
    return True


def get_deployment_containers(container_search_term: str):
    docker_client = docker.from_env()
    containers = []
    for container in docker_client.containers.list():
        if container_search_term.lower() in container.attrs.get("Name").lower():
            containers.append(container)
    return containers


def upgrade_container(old_container: Container, target_version: str = "4.0") -> str:
    """

    :param old_container: old Container object to upgrade
    :param target_version: target MongoDB version
    :return:
    """
    docker_client = docker.from_env()
    networks: Dict = old_container.attrs.get("NetworkSettings", {}).get("Networks")
    network_name = None
    if networks:
        network_name = list(networks.keys())[0]
    docker_client.containers.get(old_container.id).rename(f"{old_container.name}-{target_version}-old")
    ports = old_container.attrs.get("HostConfig", {}).get("PortBindings")
    container_id = old_container.id
    command = [old_container.attrs.get("Path"), *old_container.attrs.get("Args")]
    if "--storageEngine" not in command:
        command = [*command, "--storageEngine", "wiredTiger"]
    name = old_container.name
    old_container.stop()
    new_container = docker_client.containers.run(
        image=f"mongo:{target_version}",
        detach=True,
        volumes_from=[container_id],
        ports=ports,
        command=command,
        name=name,
        network=network_name or None
    )
    old_container.remove()
    return new_container.id


def upgrade(member_name: str, target_version: str):
    container_name = member_name.split(":")[0]
    containers = get_deployment_containers(container_name)
    if len(containers) != 1:
        raise Exception(f"Could not find exactly one container under the name '{container_name}'")
    container: Container = containers[0]
    return upgrade_container(old_container=container, target_version=target_version)


def upgrade_replica_set(replica_set_host: str, target_version: str = "4.0", docker_host: str = "local"):
    logger.info("Starting a rolling restart")
    members = list_rs_members(replica_set_host)
    logger.info(f"Initial RS state: {str(members)}")
    primary = None
    secondaries = []
    for m in members:
        state_str: str = m.get("stateStr")
        if state_str == "PRIMARY":
            primary = {**m, "upgraded": False}
        elif state_str == "SECONDARY":
            secondaries.append({**m, "upgraded": False})
        else:
            logger.info(f"{m.get('name')} is unhealthy; state: {state_str}")
    if not primary:
        logger.info("No primary in the replica set!")
    members_state = [primary, *secondaries]

    for m in [*members_state]:
        member_name = m.get("name")

        current_primary = get_primary(members)
        if current_primary.get("name") == member_name:
            step_down_primary(member_name)
        else:
            logger.info("Not a primary; no need to step down")
        container_id = upgrade(member_name=member_name, target_version=target_version)
        logger.info(f"New container ID: {container_id}")
        members = list_rs_members(replica_set_host)
        logger.info(f"Current RS state: {str(members)}")

    logger.info("Upgrade complete")
    for m in members:
        sleep(5)
        set_fcv(member_name=m.get("name"), target_version=target_version)


def get_primary(members: List) -> Dict:
    for m in members:
        state_str: str = m.get("stateStr")
        if state_str == "PRIMARY":
            return m
    raise Exception("Primary node could not be found")
