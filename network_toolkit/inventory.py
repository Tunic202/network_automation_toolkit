import yaml


def load_devices(filename="config/devices.yaml"):
    """Load network devices from a YAML inventory file."""
    with open(filename, "r") as file:
        data = yaml.safe_load(file)

    return data["devices"]
