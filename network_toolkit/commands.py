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


def verify_vlan(device, vlan_id, vlan_name):
    """Verify that a VLAN exists with the expected name."""

    logger.info(
        "Verifying VLAN %s (%s) on device '%s'.",
        vlan_id,
        vlan_name,
        device["name"],
    )

    output = run_show_command(device, "show vlan brief")

    if output is None:
        logger.error(
            "Unable to retrieve VLAN information from device '%s'.",
            device["name"],
        )
        return False

    expected = f"{vlan_id}    {vlan_name}"

    verified = expected in output

    if verified:
        logger.info(
            "VLAN %s (%s) verified successfully on device '%s'.",
            vlan_id,
            vlan_name,
            device["name"],
        )
    else:
        logger.error(
            "VLAN %s (%s) verification failed on device '%s'.",
            vlan_id,
            vlan_name,
            device["name"],
        )

    return verified


def verify_interface(device, interface, action):
    """Verify that an interface has the expected operational state."""

    logger.info(
        "Verifying interface '%s' with expected action '%s' on device '%s'.",
        interface,
        action,
        device["name"],
    )

    output = run_show_command(device, "show ip interface brief")

    if output is None:
        logger.error(
            "Unable to retrieve interface information from device '%s'.",
            device["name"],
        )
        return False

    for line in output.splitlines():
        if interface not in line:
            continue

        if action == "shutdown":
            verified = "administratively down" in line
        else:
            fields = line.split()
            verified = len(fields) >= 2 and fields[-2:] == ["up", "up"]

        if verified:
            logger.info(
                "Interface '%s' verified successfully on device '%s'.",
                interface,
                device["name"],
            )
        else:
            logger.error(
                "Interface '%s' verification failed on device '%s'.",
                interface,
                device["name"],
            )

        return verified

    logger.error(
        "Interface '%s' was not found on device '%s'.",
        interface,
        device["name"],
    )

    return False
