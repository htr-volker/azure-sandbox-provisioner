import yaml

def open_config(path: str) -> dict:
    """
    Opens a YAML file, converts it to a `dict` and returns it. Intended to be used to open the configuration
    file describing the desired state of the system.
    """
    with open(path, 'r') as stream:
        try:
            config=yaml.safe_load(stream)   
        except yaml.YAMLError as exc:
            print(exc)
    return config
