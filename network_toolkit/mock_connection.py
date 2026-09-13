class MockConnection:
    """Simulate a network device connection for testing."""

    vlan_state = {
        "cisco-router-1": {},
        "cisco-router-2": {},
    }

    interface_state = {
        "cisco-router-1": {},
        "cisco-router-2": {},
    }

    def __init__(self, device_name="cisco-router-1"):
        self.device_name = device_name

    def send_command(self, command):
        """Return simulated output for a command."""

        if command == "show version":
            if self.device_name == "cisco-router-2":
                return """
Cisco IOS Software, C2911 Software
Version 15.2(4)M6
Network Automation Lab Router 2
"""

            return """
Cisco IOS Software, C2911 Software
Version 15.2(4)M6
Network Automation Lab Router 1
"""

        if command == "show ip interface brief":
            if self.device_name == "cisco-router-2":
                interface_1_status = self.interface_state[
                    self.device_name
                ].get("GigabitEthernet0/1")

                interface_1_line = (
                    "GigabitEthernet0/1      unassigned     YES unset  "
                    "administratively down down"
                )

                if interface_1_status == "no shutdown":
                    interface_1_line = (
                        "GigabitEthernet0/1      unassigned     YES unset  "
                        "up                    up"
                    )

                return f"""
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0      192.168.2.1    YES manual up                    up
{interface_1_line}
GigabitEthernet0/2      10.10.2.1      YES manual up                    up
"""

            interface_1_status = self.interface_state[
                self.device_name
            ].get("GigabitEthernet0/1")

            interface_1_line = (
                "GigabitEthernet0/1      unassigned     YES unset  "
                "administratively down down"
            )

            if interface_1_status == "no shutdown":
                interface_1_line = (
                    "GigabitEthernet0/1      unassigned     YES unset  "
                    "up                    up"
                )

            return f"""
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0      192.168.1.1    YES manual up                    up
{interface_1_line}
GigabitEthernet0/2      unassigned     YES unset  administratively down down
"""

        if command == "show vlan brief":
            vlans = self.vlan_state[self.device_name]

            output = """
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active
"""

            for vlan_id, vlan_name in sorted(vlans.items()):
                output += (
                    f"{vlan_id}    {vlan_name:<32} active\n"
                )

            return output

        if command == "show running-config":
            vlan_config = ""

            for vlan_id, vlan_name in sorted(
                self.vlan_state[self.device_name].items()
            ):
                vlan_config += f"""
vlan {vlan_id}
 name {vlan_name}
"""

            if self.device_name == "cisco-router-2":
                return f"""
!
version 15.2
!
hostname NetworkRouter2
!
{vlan_config}
interface GigabitEthernet0/0
 ip address 192.168.2.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/2
 ip address 10.10.2.1 255.255.255.0
 no shutdown
!
ip domain-name networklab.local
!
username admin privilege 15 secret 5 $MOCKED_PASSWORD
!
end
"""

            return f"""
!
version 15.2
!
hostname NetworkRouter1
!
{vlan_config}
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
ip domain-name networklab.local
!
username admin privilege 15 secret 5 $MOCKED_PASSWORD
!
end
"""

        return f"Simulated output for: {command}"

    def send_config_set(self, commands):
        """Simulate sending configuration commands to a device."""

        print(f"Applying configuration to {self.device_name}:")

        for command in commands:
            print(f"  {command}")

        current_vlan = None
        current_interface = None

        for command in commands:
            if command.startswith("vlan "):
                current_vlan = int(command.split()[1])

            elif command.startswith("name ") and current_vlan is not None:
                vlan_name = command.split(" ", 1)[1]

                self.vlan_state[self.device_name][
                    current_vlan
                ] = vlan_name

            elif command.startswith("interface "):
                current_interface = command.split(" ", 1)[1]

            elif command in ("shutdown", "no shutdown"):
                if current_interface is not None:
                    self.interface_state[self.device_name][
                        current_interface
                    ] = command

        return "Configuration applied successfully."

    def disconnect(self):
        """Simulate closing the connection."""

        print("Mock connection closed.")
