def validate_vlan_id(vlan_id):
    """Validate a Cisco VLAN ID."""

    try:
        vlan_id = int(vlan_id)
    except ValueError:
        return False

    return 1 <= vlan_id <= 4094


def validate_vlan_name(vlan_name):
    """Validate a VLAN name."""

    if not vlan_name:
        return False

    return len(vlan_name) <= 32


def validate_interface_action(action):
    """Validate a Cisco interface action."""

    return action in ("shutdown", "no shutdown")
