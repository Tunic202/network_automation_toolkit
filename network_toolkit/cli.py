from network_toolkit.inventory import load_devices
from network_toolkit.commands import (
    get_device_version,
    get_interface_status,
    get_running_config,
    create_vlan,
    configure_interface,
    verify_vlan,
    verify_interface,
)
from network_toolkit.backup import save_running_config
from network_toolkit.validation import (
    validate_vlan_id,
    validate_vlan_name,
    validate_interface_action,
)


def select_device(devices):
    """Display devices and return the selected device."""

    print("\nAvailable devices:")

    for index, device in enumerate(devices, start=1):
        print(f"{index}. {device['name']}")

    choice = input("\nSelect a device: ")

    try:
        choice = int(choice)
    except ValueError:
        print("Invalid device selection.")
        return None

    if choice < 1 or choice > len(devices):
        print("Invalid device selection.")
        return None

    return devices[choice - 1]


def display_menu():
    """Display the main menu."""

    print("\nNetwork Automation Toolkit")
    print("==========================")
    print("1. Show device version")
    print("2. Show interface status")
    print("3. Backup running configuration")
    print("4. Create VLAN")
    print("5. Configure interface")
    print("6. Exit")


def main():
    """Run the Network Automation Toolkit."""

    display_menu()

    choice = input("\nEnter your choice: ")

    devices = load_devices()

    if choice == "1":
        device = select_device(devices)

        if device is None:
            return

        print(f"\nSelected device: {device['name']}")

        output = get_device_version(device)

        if output is not None:
            print("\nDevice version:")
            print(output)
        else:
            print("\nUnable to retrieve device version.")

    elif choice == "2":
        device = select_device(devices)

        if device is None:
            return

        print(f"\nSelected device: {device['name']}")

        output = get_interface_status(device)

        if output is not None:
            print("\nInterface status:")
            print(output)
        else:
            print("\nUnable to retrieve interface status.")

    elif choice == "3":
        device = select_device(devices)

        if device is None:
            return

        print(f"\nBacking up: {device['name']}")

        config = get_running_config(device)

        if config is not None:
            save_running_config(device, config)
        else:
            print("Unable to retrieve running configuration.")

    elif choice == "4":
        device = select_device(devices)

        if device is None:
            return

        vlan_id = input("Enter VLAN ID: ")
        vlan_name = input("Enter VLAN name: ")

        if not validate_vlan_id(vlan_id):
            print("Invalid VLAN ID. Enter a number between 1 and 4094.")
            return

        if not validate_vlan_name(vlan_name):
            print("Invalid VLAN name. It must contain 1-32 characters.")
            return

        print(f"\nConfiguring VLAN on: {device['name']}")

        output = create_vlan(device, vlan_id, vlan_name)

        if output is None:
            print("Unable to configure VLAN.")
            return

        print(output)

        print("\nVerifying VLAN configuration...")

        if verify_vlan(device, vlan_id, vlan_name):
            print("VLAN verification successful.")
        else:
            print("VLAN verification failed.")

    elif choice == "5":
        device = select_device(devices)

        if device is None:
            return

        interface = input("Enter interface name: ")
        action = input("Enter action (shutdown/no shutdown): ")

        if not validate_interface_action(action):
            print("Invalid interface action. Use 'shutdown' or 'no shutdown'.")
            return

        print(f"\nConfiguring interface on: {device['name']}")

        output = configure_interface(
            device,
            interface,
            action,
        )

        if output is None:
            print("Unable to configure interface.")
            return

        print(output)

        print("\nVerifying interface configuration...")

        if verify_interface(device, interface, action):
            print("Interface verification successful.")
        else:
            print("Interface verification failed.")

    elif choice == "6":
        print("Goodbye!")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
