class MockConnection:
    """Simulate a network device connection for testing."""

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
                return """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0      192.168.2.1    YES manual up                    up
GigabitEthernet0/1      unassigned     YES unset  administratively down down
GigabitEthernet0/2      10.10.2.1      YES manual up                    up
"""

            return """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0      192.168.1.1    YES manual up                    up
GigabitEthernet0/1      unassigned     YES unset  administratively down down
GigabitEthernet0/2      unassigned     YES unset  administratively down down
"""

        if command == "show running-config":
            if self.device_name == "cisco-router-2":
                return """
!
version 15.2
!
hostname NetworkRouter2
!
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

            return """
!
version 15.2
!
hostname NetworkRouter1
!
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

        return "Configuration applied successfully."

    def disconnect(self):
        """Simulate closing the connection."""

        print("Mock connection closed.")
