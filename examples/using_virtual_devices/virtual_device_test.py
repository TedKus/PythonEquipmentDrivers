import pythonequipmentdrivers as ped
from pathlib import Path


def test_source_operations(source):
    """Test various source operations"""
    print("\n=== Testing Source Operations ===")

    # Test voltage operations
    print("\nVoltage Operations:")
    source.set_voltage(12.0)
    voltage = source.measure_voltage()
    print(f"Set voltage: 12.0V, Measured: {voltage}V")

    # Test current operations
    print("\nCurrent Operations:")
    source.set_current(2.0)
    current = source.measure_current()
    print(f"Set current: 2.0A, Measured: {current}A")

    # Test power state
    print("\nPower State Operations:")
    source.on()
    source.off()

    # Check call history
    history = source.get_call_history()
    print("\nSource Call History:")
    for method, args in history.items():
        print(f"Method: {method}, Args: {args}")


def test_sink_operations(sink):
    """Test various sink operations"""
    print("\n=== Testing Sink Operations ===")

    # Test current operations
    print("\nCurrent Operations:")
    sink.set_current(1.0)
    current = sink.measure_current()
    print(f"Set current: 1.0A, Measured: {current}A")

    # Test mode operations
    print("\nMode Operations:")
    sink.set_mode("CC")

    # Test custom measurement values
    print("\nCustom Measurement Test:")
    sink.set_measurement_value("measure_voltage", 24.0)
    voltage = sink.measure_voltage()
    print(f"Custom voltage measurement: {voltage}V")


def test_multimeter_operations(dmm):
    """Test various multimeter operations"""
    print("\n=== Testing Multimeter Operations ===")

    # Test voltage measurements
    print("\nVoltage Measurements:")
    dmm.set_mode("VDC")
    voltage = dmm.measure_voltage()
    print(f"Measured voltage: {voltage}V")

    # Test custom measurements
    print("\nCustom Measurement Test:")
    dmm.set_measurement_value("measure_voltage", 5.0)
    voltage = dmm.measure_voltage()
    print(f"Custom voltage measurement: {voltage}V")


def main():
    # Load Virtual devices configuration
    config_path = Path(__file__).parent / "new_virtual_config.json"
    equipment = ped.connect_resources(config=config_path, init=True)

    # Test each virtual device
    test_source_operations(equipment.virtual_source)
    test_sink_operations(equipment.virtual_sink)
    test_multimeter_operations(equipment.virtual_multimeter)

    # Demonstrate error handling
    print("\n=== Testing Error Handling ===")
    try:
        equipment.virtual_source.invalid_method()
    except Exception as e:
        print(f"Caught expected error for invalid method: {e}")

    # Test device state persistence
    print("\n=== Testing State Persistence ===")
    equipment.virtual_source.set_voltage(15.0)
    print(f"Voltage after setting: {equipment.virtual_source.measure_voltage()}V")
    print(f"Voltage using get_voltage: {equipment.virtual_source.get_voltage()}V")

    print("\nTest completed successfully!")


if __name__ == "__main__":
    main()
