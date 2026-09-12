# Network Automation Toolkit

A Python-based network automation toolkit for managing Cisco-style network devices through a command-line interface (CLI).

The project is being developed as a practical network-engineering automation portfolio project, with a focus on Python, Netmiko, device inventory management, configuration backups, validation, logging, automated testing, and safe development using simulated devices.

## Project Status

Core functionality is implemented and tested.

**Current test suite: 19 tests passing**

The project currently supports simulated Cisco devices and is structured so that the same automation functions can later be used with real network devices through Netmiko.

## Features

- YAML-based device inventory
- Multiple-device selection
- Cisco IOS device version retrieval
- Interface status retrieval with `show ip interface brief`
- Running configuration retrieval
- Timestamped running-configuration backups
- VLAN creation
- Interface configuration with `shutdown` and `no shutdown`
- Input validation for VLANs and interface actions
- Application logging
- SSH connection handling with Netmiko
- Mock device connections for safe development and testing
- Automated unit tests with Python `unittest`
- Clear handling of connection timeouts and authentication failures

## Technologies

- Python
- Netmiko
- PyYAML
- python-dotenv
- `unittest`
- YAML
- Git and GitHub

## Project Structure

```text
network_automation_toolkit/
│
├── config/
│   └── devices.yaml
│
├── network_toolkit/
│   ├── __init__.py
│   ├── backup.py
│   ├── cli.py
│   ├── commands.py
│   ├── connection.py
│   ├── inventory.py
│   ├── logger.py
│   ├── mock_connection.py
│   └── validation.py
│
├── tests/
│   ├── test_backup.py
│   ├── test_commands.py
│   ├── test_inventory.py
│   └── test_validation.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

The toolkit separates the main responsibilities of the application into small Python modules.

```text
                 ┌──────────────────┐
                 │       CLI        │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │    Inventory     │
                 │   devices.yaml   │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │    Connection    │
                 │ Netmiko / Mock   │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │     Commands     │
                 │ show / configure │
                 └──────┬─────┬──────┘
                        │     │
              ┌─────────▼─┐ ┌─▼──────────┐
              │  Backups  │ │   Logger   │
              └───────────┘ └────────────┘
```

## Current CLI Operations

When the toolkit is started, the available operations are:

```text
Network Automation Toolkit
==========================
1. Show device version
2. Show interface status
3. Backup running configuration
4. Create VLAN
5. Configure interface
6. Exit
```

Each operation requires selecting a device from the inventory where appropriate.

## Example: Show Device Version

```text
Available devices:
1. cisco-router-1
2. cisco-router-2

Select a device: 2

Selected device: cisco-router-2

Using mock connection.

Device version:

Cisco IOS Software, C2911 Software
Version 15.2(4)M6
Network Automation Lab Router 2
```

## Example: Interface Status

The toolkit can retrieve Cisco-style interface information:

```text
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0      192.168.2.1    YES manual up                    up
GigabitEthernet0/1      unassigned     YES unset  administratively down down
GigabitEthernet0/2      10.10.2.1      YES manual up                    up
```

## Example: VLAN Configuration

A VLAN can be created through the CLI:

```text
Enter VLAN ID: 10
Enter VLAN name: USERS

Configuring VLAN on: cisco-router-1

Using mock connection.

Applying configuration to cisco-router-1:
  vlan 10
  name USERS

Configuration applied successfully.
```

The toolkit validates the VLAN ID before sending configuration to the device. VLAN IDs outside the accepted range are rejected, and empty VLAN names are rejected.

## Example: Interface Configuration

The toolkit can simulate enabling or disabling an interface:

```text
Enter interface name: GigabitEthernet0/1
Enter action (shutdown/no shutdown): shutdown

Configuring interface on: cisco-router-1

Using mock connection.

Applying configuration to cisco-router-1:
  interface GigabitEthernet0/1
  shutdown

Configuration applied successfully.
```

Only the supported `shutdown` and `no shutdown` actions are accepted by the validation layer.

## Configuration Backups

Running configurations are saved with timestamps so that previous backups are preserved rather than overwritten.

Example:

```text
backups/
└── cisco-router-1_2026-09-12_22-13-36_running_config.txt
```

Backup operations are also recorded in the application log.

## Logging

Application activity is written to:

```text
logs/network_toolkit.log
```

The log records events such as:

- Device connection attempts
- Successful command execution
- Configuration changes
- Backup operations
- Connection failures

Example:

```text
2026-09-12 21:09:55,156 - INFO - Running command 'show ip interface brief' on device 'cisco-router-1'.
2026-09-12 21:09:55,156 - INFO - Command 'show ip interface brief' completed successfully on device 'cisco-router-1'.
2026-09-12 21:17:32,546 - ERROR - Connection timed out for device 'unreachable-router'.
```

Logs and generated backups are excluded from version control by `.gitignore`.

## Mock Device Mode

The project includes a mock connection layer so that network automation functionality can be developed and tested without requiring a physical Cisco router or switch.

The inventory can mark a device with:

```yaml
mock: true
```

Mock devices return realistic Cisco-style command output and simulate configuration changes.

This provides a safe development workflow before connecting the toolkit to real network infrastructure.

## Using Real Devices

The connection layer is designed to support Netmiko for real network devices.

Real credentials should not be hard-coded into the source code. The application is structured to obtain the network username and password from environment variables.

Example environment variables:

```text
NETWORK_USERNAME=your_username
NETWORK_PASSWORD=your_password
```

Do not commit `.env` files or real credentials to GitHub.

Before using the toolkit against production infrastructure, test configuration changes in a controlled lab environment and verify device-specific command requirements.

## Installation

Clone the repository:

```bash
git clone https://github.com/Tunic202/network_automation_toolkit.git
cd network_automation_toolkit
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Running the Toolkit

Start the CLI with:

```bash
python -m network_toolkit.cli
```

## Running the Tests

Run the complete automated test suite with:

```bash
python -m unittest discover -s tests -v
```

Current result:

```text
Ran 19 tests
OK
```

The tests cover inventory loading, command retrieval, configuration changes, backups, and input validation.

## Testing Connection Failures

The connection module handles Netmiko timeout and authentication exceptions and reports useful messages instead of allowing the program to crash unexpectedly.

Example timeout message:

```text
Connection timed out. Check the device IP and network connection.
```

The failure is also recorded in the application log.

## Development Approach

The project is being developed incrementally:

1. Build and test individual automation functions.
2. Use mock devices to avoid depending on live infrastructure.
3. Add validation before configuration changes.
4. Add logging for troubleshooting and auditability.
5. Add automated tests as new capabilities are introduced.
6. Commit stable milestones to GitHub.
7. Extend the toolkit toward real-device automation.

## Future Improvements

Planned enhancements include:

- Real-device testing with Cisco IOS/IOS-XE lab equipment
- Batch operations across selected devices
- More interface configuration options
- VLAN verification after configuration
- Configuration diffing
- Backup restore workflows
- CSV/JSON reporting
- Richer CLI output
- Continuous integration with GitHub Actions
- API access for automation from other applications
- Additional network platforms such as Juniper or Arista

## Repository

GitHub: https://github.com/Tunic202/network_automation_toolkit

## Author

**Theophilus Usifo**
