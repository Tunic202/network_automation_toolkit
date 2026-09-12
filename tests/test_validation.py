import unittest

from network_toolkit.validation import (
    validate_vlan_id,
    validate_vlan_name,
    validate_interface_action,
)


class TestValidation(unittest.TestCase):
    """Test network configuration input validation."""

    def test_valid_vlan_id(self):
        """Test a valid VLAN ID."""

        self.assertTrue(validate_vlan_id(10))

    def test_minimum_vlan_id(self):
        """Test the minimum accepted VLAN ID."""

        self.assertTrue(validate_vlan_id(1))

    def test_maximum_vlan_id(self):
        """Test the maximum accepted VLAN ID."""

        self.assertTrue(validate_vlan_id(4094))

    def test_invalid_vlan_id(self):
        """Test an invalid VLAN ID."""

        self.assertFalse(validate_vlan_id(5000))

    def test_vlan_id_below_range(self):
        """Test a VLAN ID below the accepted range."""

        self.assertFalse(validate_vlan_id(0))

    def test_vlan_id_above_range(self):
        """Test a VLAN ID above the accepted range."""

        self.assertFalse(validate_vlan_id(4095))

    def test_valid_vlan_name(self):
        """Test a valid VLAN name."""

        self.assertTrue(validate_vlan_name("USERS"))

    def test_empty_vlan_name(self):
        """Test an empty VLAN name."""

        self.assertFalse(validate_vlan_name(""))

    def test_valid_shutdown_action(self):
        """Test the shutdown interface action."""

        self.assertTrue(validate_interface_action("shutdown"))

    def test_valid_no_shutdown_action(self):
        """Test the no shutdown interface action."""

        self.assertTrue(validate_interface_action("no shutdown"))

    def test_invalid_interface_action(self):
        """Test an invalid interface action."""

        self.assertFalse(validate_interface_action("reload"))


if __name__ == "__main__":
    unittest.main()
