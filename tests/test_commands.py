import unittest

from network_toolkit.commands import (
    get_device_version,
    get_interface_status,
    get_running_config,
    create_vlan,
    configure_interface,
)


TEST_DEVICE = {
    "name": "cisco-router-1",
    "mock": True,
}


class TestCommands(unittest.TestCase):
    """Test network automation command functions."""

    def test_get_device_version(self):
        """Test retrieving the device version."""

        output = get_device_version(TEST_DEVICE)

        self.assertIn("Cisco IOS Software", output)
        self.assertIn("Version 15.2(4)M6", output)
        self.assertIn("Network Automation Lab Router 1", output)

    def test_get_interface_status(self):
        """Test retrieving interface status."""

        output = get_interface_status(TEST_DEVICE)

        self.assertIn("GigabitEthernet0/0", output)
        self.assertIn("192.168.1.1", output)
        self.assertIn("up", output)

    def test_get_running_config(self):
        """Test retrieving the running configuration."""

        output = get_running_config(TEST_DEVICE)

        self.assertIn("hostname NetworkRouter1", output)
        self.assertIn("192.168.1.1", output)
        self.assertIn("no shutdown", output)

    def test_create_vlan(self):
        """Test creating a VLAN."""

        output = create_vlan(TEST_DEVICE, 10, "USERS")

        self.assertEqual(output, "Configuration applied successfully.")

    def test_configure_interface(self):
        """Test configuring a network interface."""

        output = configure_interface(
            TEST_DEVICE,
            "GigabitEthernet0/1",
            "shutdown",
        )

        self.assertEqual(output, "Configuration applied successfully.")


if __name__ == "__main__":
    unittest.main()
