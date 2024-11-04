from typing import List, Tuple, Dict
import re
import json
from collections import defaultdict

from pythonequipmentdrivers import (source,
                                    sink,
                                    multimeter,
                                    daq,
                                    powermeter,
                                    oscilloscope,
                                    networkanalyzer,
                                    functiongenerator,
                                    temperaturecontroller)


def get_available_devices() -> Dict[str, List[str]]:
    """
    Returns a dictionary of all available device types and their
    corresponding device names.

    Returns:
        Dict[str, List[str]]: Dictionary with device types as keys and
        lists of device names as values
    """
    modules = {
        'source': source,
        'sink': sink,
        'multimeter': multimeter,
        'daq': daq,
        'powermeter': powermeter,
        'oscilloscope': oscilloscope,
        'networkanalyzer': networkanalyzer,
        'functiongenerator': functiongenerator,
        'temperaturecontroller': temperaturecontroller
    }

    available_devices = {}

    for module_name, module in modules.items():
        if hasattr(module, '__all__'):
            available_devices[module_name] = module.__all__

    return available_devices


def print_available_devices():
    """
    Prints all available devices organized by type.
    """
    devices = get_available_devices()

    print("Available Devices:")
    for device_type, device_list in devices.items():
        print(f"\n{device_type.upper()}:")
        for device in device_list:
            print(f"  - {device}")


def get_connected_devices(
        visa_resources: List[Tuple[str, str]] = None
        ) -> Dict[str, List[Tuple[str, str]]]:
    """
    Returns a dictionary of connected devices matched with their driver
    classes.

    Args:
        visa_resources: Optional list of VISA resources. If None, will call
        identify_visa_resources()

    Returns:
        Dict[str, List[Tuple[str, str]]]: Dictionary with device types as keys
        and lists of tuples (address, model) as values
    """
    from pythonequipmentdrivers import identify_visa_resources

    # Get all available device classes
    available_devices = get_available_devices()

    # Get VISA resources if not provided
    if visa_resources is None:
        visa_resources = identify_visa_resources()

    # Initialize result dictionary
    connected_devices = {category: [] for category in available_devices.keys()}

    def normalize_string(s: str) -> str:
        """Remove spaces, punctuation, and convert to lowercase"""
        return re.sub(r'[_\s\-,.:;()"]', '', s.lower())

    # Create device lookup patterns
    device_lookup = {}
    for category, devices in available_devices.items():
        for device in devices:
            normalized = normalize_string(device)
            if 'dpo4xxx' in normalized:
                # Special case for oscilloscopes
                pattern = normalized.replace('dpo4xxx', '[dm]do4.*')
            elif 'mso5xxx' in normalized:
                pattern = normalized.replace('dpo5xxx', '[dm]do5.*')
            else:
                # Extract model number for general matching
                model_match = re.search(r'\d+[a-zA-Z]*', normalized)
                if model_match:
                    pattern = model_match.group()
                else:
                    pattern = normalized.replace('xxx', '.*')
            device_lookup[pattern] = (category, device)

    # Process each VISA resource
    for address, description in visa_resources:
        normalized_desc = normalize_string(description)

        for pattern, (category, original_name) in device_lookup.items():
            if re.search(pattern, normalized_desc):
                connected_devices[category].append((address, original_name))
                break

    return connected_devices


def print_connected_devices():
    """
    Prints all connected devices organized by type.
    Get connected devices:
    connected = get_connected_devices()

    Print in a formatted way:
    print_connected_devices()
    """
    devices = get_connected_devices()

    print("Connected Devices:")
    for device_type, device_list in devices.items():
        if device_list:  # Only print categories that have connected devices
            print(f"\n{device_type.upper()}:")
            for address, model in device_list:
                print(f"  - {model}")
                print(f"    Address: {address}")


def generate_equipment_config(output_file: str = "equipment.config",
                            visa_resources: List[Tuple[str, str]] = None) -> None:
    """
    Generates an equipment configuration file from connected devices.

    Args:
        output_file (str): Path to the output configuration file
        visa_resources: Optional list of VISA resources. If None, will call
        identify_visa_resources()
    """

    # Load default init configurations
    # Default initialization commands for different device types
    # Safety-critical defaults for new setups
    # default_init_path = Path(__file__).parent / "default_init_config.json"
    # with open(default_init_path, 'r') as f:
    #     default_init = json.load(f)
    default_init = {
        "source": [
            ["set_voltage", {"voltage": 0}],
            ["off", {}],
            ["set_current", {"current": 0}]
        ],
        "sink": [
            ["off", {}],
            ["set_mode", {"mode": "CC"}],
            ["set_current", {"current": 0}]
        ],
        "multimeter": [
            ["set_mode", {"mode": "VDC"}]
        ],
        "oscilloscope": [
            ["set_channel_coupling", {"channel": 1, "coupling": "dc"}]
        ],
        "functiongenerator": [
            ["set_voltage_amplitude", {"voltage": 0}],
            ["off", {}]
        ],
        "powermeter": [
            ["set_integration_time", {"time": 0.1}]
        ]
    }

    # Get connected devices
    connected = get_connected_devices(visa_resources)

    # Create config dictionary
    config = {}

    # Counter for multiple devices of the same type
    type_counters = defaultdict(int)

    # Process each connected device
    for category, devices in connected.items():
        for address, model in devices:
            # Generate a unique name for this device
            type_counters[category] += 1
            count = type_counters[category]
            device_name = f"{category}{count}" if count > 1 else category

            # Create device configuration
            device_config = {
                "object": model,
                "definition": f"pythonequipmentdrivers.{category}",
                "address": address
            }

            # Add initialization commands if available
            if category in default_init:
                device_config["init"] = default_init[category]

            config[device_name] = device_config

    # Custom JSON formatting
    def format_json(obj, indent=4):
        if isinstance(obj, dict):
            # For simple single-line dictionaries (like parameter dicts)
            if len(obj) == 1 and all(not isinstance(v, (dict, list)) for v in obj.values()):
                return json.dumps(obj)
            # For more complex dictionaries
            items = []
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    items.append(f'{" " * indent}"{k}": {format_json(v, indent + 4)}')
                else:
                    items.append(f'{" " * indent}"{k}": {json.dumps(v)}')
            return "{\n" + ",\n".join(items) + "\n" + " " * (indent - 4) + "}"
        elif isinstance(obj, list):
            # For lists of command pairs
            if all(isinstance(x, list) and len(x) == 2 for x in obj):
                items = []
                for cmd, params in obj:
                    items.append(f'{" " * indent}["{cmd}", {json.dumps(params)}]')
                return "[\n" + ",\n".join(items) + "\n" + " " * (indent - 4) + "]"
            # For other lists
            return json.dumps(obj)
        return json.dumps(obj)

    # Write to file with custom formatting
    with open(output_file, 'w') as f:
        f.write(format_json(config))

    print(f"Configuration file generated: {output_file}")

    # Also print the configuration to console
    print("\nGenerated Configuration:")
    print(format_json(config))
