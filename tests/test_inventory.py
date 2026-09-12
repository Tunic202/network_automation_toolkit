import unittest

from network_toolkit.inventory import load_devices


class TestInventory(unittest.TestCase):
    """Test network device inventory."""

    def test_load_devices(self):
        """Test that devices are loaded from the YAML inventory."""

        devices = load_devices()

        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]["name"], "cisco-router-1")
        self.assertEqual(devices[1]["name"], "cisco-router-2")
        self.assertTrue(devices[0]["mock"])
        self.assertTrue(devices[1]["mock"])

    def test_load_devices_contains_expected_hosts(self):
        """Test that the inventory contains the expected device IP addresses."""

        devices = load_devices()

        self.assertEqual(devices[0]["host"], "192.168.1.1")
        self.assertEqual(devices[1]["host"], "192.168.1.2")


if __name__ == "__main__":
    unittest.main()
