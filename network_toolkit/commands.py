from network_toolkit.connection import connect_to_device
from network_toolkit.logger import get_logger


logger = get_logger()


def run_show_command(device, command):
    """Run a read-only show command on a network device."""

    logger.info(
        "Running command '%s' on device '%s'.",
        command,
        device["name"],
    )

    connection = connect_to_device(device)

    if connection is None:
        logger.error(
            "Unable to connect to device '%s'.",
            device["name"],
        )
        return None

    output = connection.send_command(command)

    connection.disconnect()

    logger.info(
        "Command '%s' completed successfully on device '%s'.",
        command,
        device["name"],
    )

    return output


def get_device_version(device):
    """Retrieve the Cisco IOS version from a device."""

    return run_show_command(device, "show version")


def get_interface_status(device):
    """Retrieve interface status from a device."""

    return run_show_command(device, "show ip interface brief")


def get_running_config(device):
    """Retrieve the running configuration from a device."""

    return run_show_command(device, "show running-config")


def create_vlan(device, vlan_id, vlan_name):
    """Create a VLAN on a network device."""

    logger.info(
        "Creating VLAN %s (%s) on device '%s'.",
        vlan_id,
        vlan_name,
        device["name"],
    )

    connection = connect_to_device(device)

    if connection is None:
        logger.error(
            "Unable to connect to device '%s' for VLAN configuration.",
            device["name"],
        )
        return None

    configuration = [
        f"vlan {vlan_id}",
        f"name {vlan_name}",
    ]

    output = connection.send_config_set(configuration)

    connection.disconnect()

    logger.info(
        "VLAN %s (%s) configured successfully on device '%s'.",
        vlan_id,
        vlan_name,
        device["name"],
    )

    return output


def configure_interface(device, interface, action):
    """Enable or disable a network interface."""

    logger.info(
        "Configuring interface '%s' with action '%s' on device '%s'.",
        interface,
        action,
        device["name"],
    )

    connection = connect_to_device(device)

    if connection is None:
        logger.error(
            "Unable to connect to device '%s' for interface configuration.",
            device["name"],
        )
        return None

    configuration = [
        f"interface {interface}",
        action,
    ]

    output = connection.send_config_set(configuration)

    connection.disconnect()

    logger.info(
        "Interface '%s' configured with action '%s' on device '%s'.",
        interface,
        action,
        device["name"],
    )

    return output
