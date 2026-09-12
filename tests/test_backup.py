import unittest

from network_toolkit.backup import save_running_config


class TestBackup(unittest.TestCase):
    """Test configuration backup functionality."""

    def test_save_running_config(self):
        """Test that a running configuration is saved to a timestamped file."""

        device = {
            "name": "test-router",
            "mock": True,
        }

        config = """
hostname TestRouter
interface GigabitEthernet0/0
 ip address 192.168.10.1 255.255.255.0
 no shutdown
"""

        backup_file = save_running_config(device, config)

        self.assertTrue(backup_file.exists())
        self.assertEqual(backup_file.read_text(), config)
        self.assertIn("test-router_", backup_file.name)
        self.assertIn("_running_config.txt", backup_file.name)

        backup_file.unlink()


if __name__ == "__main__":
    unittest.main()
