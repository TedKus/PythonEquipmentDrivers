import pythonequipmentdrivers as ped
from pathlib import Path


def main():
    # Load dummy devices configuration
    config_path = Path(__file__).parent / "dummy_config.json"
    equipment = ped.connect_resources(config=config_path, init=True)

    # Example usage of dummy devices
    print("\n=== Testing Dummy Devices ===")

    # Source operations
    print("\nSource Operations:")
    equipment.dummy_source.set_voltage(12.0)
    voltage = equipment.dummy_source.measure_voltage()
    print(f"Set voltage: 12.0V, Measured: {voltage}V")

    # Sink operations
    print("\nSink Operations:")
    equipment.dummy_sink.set_current(1.0)
    current = equipment.dummy_sink.measure_current()
    print(f"Set current: 1.0A, Measured: {current}A")

    # Multimeter operations
    print("\nMultimeter Operations:")
    voltage = equipment.dummy_multimeter.measure_voltage()
    print(f"Measured voltage: {voltage}V")

    # More device operations can be added here...


if __name__ == "__main__":
    main()
