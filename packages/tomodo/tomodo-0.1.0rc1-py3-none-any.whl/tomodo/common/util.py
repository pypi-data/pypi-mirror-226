def parse_semver(version_str: str) -> (str, str, str):
    try:
        [maj_v, min_v, patch] = version_str.split(".")
        return int(maj_v), int(min_v), patch
    except ValueError:
        pass
    try:
        [maj_v, min_v] = version_str.split(".")
        return int(maj_v), int(min_v), None
    except ValueError:
        raise
