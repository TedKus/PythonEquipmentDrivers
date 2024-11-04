from pathlib import Path
from pythonequipmentdrivers.utility.equipment_finder import (
    print_available_devices,
    print_connected_devices,
    generate_equipment_config)


def main():
    # Print all available device types and models
    print("\n=== Available Devices ===")
    print_available_devices()

    # Print currently connected devices
    print("\n=== Connected Devices ===")
    print_connected_devices()

    # Generate a configuration file in the same directory as this script
    config_path = Path(__file__).parent / "discovered_equipment.config"
    print("\n=== Generating Configuration File ===")
    generate_equipment_config(config_path)
    print(f"Configuration file saved to: {config_path}")


if __name__ == "__main__":
    main()
