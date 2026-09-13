import os

from dotenv import load_dotenv
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

from network_toolkit.logger import get_logger
from network_toolkit.mock_connection import MockConnection


load_dotenv()

logger = get_logger()


def connect_to_device(device):
    """Connect to a network device using SSH or mock mode."""

    if device.get("mock"):
        logger.info(
            "Using mock connection for device '%s'.",
            device.get("name", "unknown"),
        )
        print("Using mock connection.")
        return MockConnection(device.get("name"))

    device_config = device.copy()

    device_config.pop("name", None)
    device_config.pop("mock", None)

    username = os.getenv("NETWORK_USERNAME")
    password = os.getenv("NETWORK_PASSWORD")
    secret = os.getenv("NETWORK_SECRET")

    if not username or not password:
        logger.error(
            "Network credentials are missing for device '%s'.",
            device.get("name", "unknown"),
        )
        print("Network credentials are missing. Check your .env file.")
        return None

    device_config["username"] = username
    device_config["password"] = password

    if secret:
        device_config["secret"] = secret

    try:
        logger.info(
            "Attempting SSH connection to device '%s' at %s.",
            device.get("name", "unknown"),
            device_config.get("host"),
        )

        connection = ConnectHandler(**device_config)

        if secret:
            connection.enable()

        logger.info(
            "Successfully connected to device '%s'.",
            device.get("name", "unknown"),
        )

        return connection

    except NetmikoAuthenticationException:
        logger.error(
            "Authentication failed for device '%s'.",
            device.get("name", "unknown"),
        )
        print("Authentication failed. Check the username and password.")

    except NetmikoTimeoutException:
        logger.error(
            "Connection timed out for device '%s'.",
            device.get("name", "unknown"),
        )
        print("Connection timed out. Check the device IP and network connection.")

    except Exception as error:
        logger.exception(
            "Unexpected connection error for device '%s': %s",
            device.get("name", "unknown"),
            error,
        )
        print(f"Connection error: {error}")

    return None
