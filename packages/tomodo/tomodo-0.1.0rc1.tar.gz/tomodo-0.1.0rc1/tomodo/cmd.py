import logging

import typer
from rich.console import Console
from rich.logging import RichHandler

from tomodo.common.upgrader import upgrade_replica_set, get_mongodb_version
from tomodo.common.util import parse_semver

console = Console()

logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("rich")

UPGRADE_VERSION_PATH = {
    "3.6": "4.0",
    "4.0": "4.2",
    "4.2": "4.4",
    "4.4": "5.0",
    "5.0": "6.0",
    "6.0": "7.0",
}


def upgrade(hostname: str, target_version: str = "6.0", replica_set: bool = True, docker_host: str = "local"):
    """
    Upgrade a MongoDB Standalone Instance or Replica Set to a target version.
    """
    target_maj, target_min, _ = parse_semver(target_version)
    target_min = f"{target_maj}.{target_min}"
    current_version = get_mongodb_version(host=hostname)
    current_maj, current_min, current_patch = parse_semver(current_version)
    current_min = f"{current_maj}.{current_min}"
    logger.info(f"This will upgrade {hostname} from {current_min} to {target_min}")

    upgrade_path = []
    append = False
    for v_from, v_to in UPGRADE_VERSION_PATH.items():
        if target_min == v_to:
            upgrade_path.append(target_version)
            break
        if v_from == current_min:
            append = True
        if append:
            upgrade_path.append(v_to)
    logger.info(f"The upgrade path is {current_version} --> {' --> '.join(upgrade_path)}.")
    logger.info(f"This means that {len(upgrade_path)} upgrades will be performed serially.")
    for next_version in upgrade_path:
        if replica_set:
            logger.info(f"Now upgrading replica set from version {current_version} to {next_version}")
            upgrade_replica_set(replica_set_host=hostname, target_version=next_version)
            logger.info(f"Upgraded to {next_version} successfully.")
            current_version = get_mongodb_version(host=hostname)
        else:
            pass


def run():
    typer.run(upgrade)
