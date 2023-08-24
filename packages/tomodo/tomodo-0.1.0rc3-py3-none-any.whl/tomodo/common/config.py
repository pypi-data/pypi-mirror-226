from ruamel.yaml import YAML, yaml_object

yaml = YAML()


class Replica:
    def __init__(self, connection_string: str, docker_host: str = "local"):
        self.connection_string: str = connection_string
        self.docker_host: str = docker_host

    def __repr__(self):
        return f"""
  connection_string: {self.connection_string}
  docker_host: {self.docker_host}
        """


@yaml_object(yaml)
class Config:
    def __init__(self, target_version: str, standalone: bool, hostname: str = None, replicas: [Replica] = None):
        self.target_version = target_version
        self.standalone = standalone
        self.hostname = hostname
        if replicas:
            self.replicas = [Replica(**r) for r in replicas]

    def __repr__(self):
        return f"""target_version: {self.target_version}
standalone: {self.standalone}
hostname: {self.hostname}
replicas: {str(self.replicas or "")}
        """


def from_file(file_path: str):
    pass


if __name__ == "__main__":
    yaml_str = """
target_version: 4.3.1
standalone: false
replicas:
  - connection_string: foo1
    docker_host: bar1
  - connection_string: foo2
    docker_host: bar2
    """
    res = yaml.load(yaml_str)
    print(str(Config(**res)))
