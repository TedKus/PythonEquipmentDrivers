from .Keithley_2231A import Keithley_2231A


# acts as an alias of Keithley_2231A
class Sorensen_XBT(Keithley_2231A):
    """
    Sorensen_XBT(address)

    address : str, address of the connected power supply

    object for accessing basic functionality of the Sorensen_XBT DC supply
    """

    def set_over_voltage_protection(self, voltage: float) -> None:
        """
        set_over_voltage_protection(voltage)

        Configures the OVP set point of the supply.

        Args:
            voltage (float): Over voltage protection set-point in Volts DC.
        """

        self.write_resource(f"SOUR:VOLT:PROT {float(voltage)}")

    def get_over_voltage_protection(self) -> float:
        """
        get_over_voltage_protection(voltage)

        Retrieve the current value of the OVP set point of the supply.

        Returns:
            float: Over voltage protection set-point in Volts DC.
        """

        response = self.query_resource("SOUR:VOLT:PROT?")
        return float(response)

    def set_over_current_protection(self, current: float) -> None:
        """
        set_over_current_protection(current)

        Configures the OCP set point of the supply.

        Args:
            current (float): Over current protection set-point in Amps DC.
        """

        self.write_resource(f"SOUR:CURR:LIM {current}")

    def get_over_current_protection(self) -> float:
        """
        get_over_current_protection(current)

        Retrieve the current value of the OCP set point of the supply.

        Returns:
            float: Over current protection set-point in Amps DC.
        """

        response = self.query_resource("SOUR:CURR:LIM?")
        return float(response)


if __name__ == "__main__":
    pass
