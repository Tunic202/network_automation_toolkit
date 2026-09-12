from datetime import datetime
from pathlib import Path

from network_toolkit.logger import get_logger


logger = get_logger()


def save_running_config(device, config):
    """Save a device's running configuration to a timestamped backup file."""

    backup_directory = Path("backups")
    backup_directory.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = (
        backup_directory
        / f"{device['name']}_{timestamp}_running_config.txt"
    )

    logger.info(
        "Saving running configuration for device '%s'.",
        device["name"],
    )

    filename.write_text(config)

    logger.info(
        "Backup completed for device '%s': %s",
        device["name"],
        filename,
    )

    print(f"Backup saved to: {filename}")

    return filename
