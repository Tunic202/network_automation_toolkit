import unittest

from network_toolkit.commands import (
    create_vlan,
    verify_vlan,
    configure_interface,
    verify_interface,
)


TEST_DEVICE = {
    "name": "cisco-router-1",
    "mock": True,
}


class TestVerification(unittest.TestCase):
    """Test post-configuration verification."""

    def test_verify_vlan(self):
        """Test that a newly created VLAN is verified successfully."""

        create_vlan(TEST_DEVICE, 30, "TEST_VLAN")

        result = verify_vlan(
            TEST_DEVICE,
            30,
            "TEST_VLAN",
        )

        self.assertTrue(result)

    def test_verify_interface_shutdown(self):
        """Test verification of a shutdown interface."""

        configure_interface(
            TEST_DEVICE,
            "GigabitEthernet0/1",
            "shutdown",
        )

        result = verify_interface(
            TEST_DEVICE,
            "GigabitEthernet0/1",
            "shutdown",
        )

        self.assertTrue(result)

    def test_verify_interface_no_shutdown(self):
        """Test verification of an enabled interface."""

        configure_interface(
            TEST_DEVICE,
            "GigabitEthernet0/1",
            "no shutdown",
        )

        result = verify_interface(
            TEST_DEVICE,
            "GigabitEthernet0/1",
            "no shutdown",
        )

        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
