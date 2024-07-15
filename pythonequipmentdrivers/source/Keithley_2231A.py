from ..core import VisaResource
from typing import List, Union


class Keithley_2231A(VisaResource):
    """
    Keithley_2231A(address, channel)

    address : str, address of the connected power supply
    channel : int, if not None this instance will be associated
        with a particular output channel. The channel argument will no longer
        need to be supplied for any subsequent method call. However, supplying
        the channel argument will override the channel that is associated
        with the instance.


    object for accessing basic functionality of the Keithley DC supply
    """

    def __init__(self, address: str, channel: int = None, **kwargs) -> None:
        super().__init__(address, **kwargs)
        self.channel = channel
        self.set_access_remote("remote")

    def __del__(self) -> None:
        self.set_access_remote("local")
        super().__del__()

    def set_access_remote(self, mode: str) -> None:
        """
        set_access_remote(mode)

        mode: str, interface method either 'remote' or 'local'

        set access to the device interface to 'remote' or 'local'
        """

        if mode.lower() == "remote":
            self.write_resource("SYSTem:RWLock")
        elif mode.lower() == "local":
            self.write_resource("SYSTem:LOCal")
        else:
            raise ValueError(
                'Unknown option for arg "mode", should be "remote" or "local"'
            )

    def set_channel(self, channel: int) -> None:
        """
        set_channel(channel)

        channel: int, index of the channel to control.
                 valid options are 1-3

        Selects the specified Channel to use for software control
        """

        self.write_resource(f"INST:NSEL {channel}")

    def _update_channel(self, override_channel):
        """Handles updating the device channel setting"""

        if override_channel is not None:
            self.set_channel(override_channel)
        elif self.channel is not None:
            self.set_channel(self.channel)
        else:
            raise TypeError(
                "Channel number must be provided if it is not provided during"
                + "initialization"
            )
        return

    def get_channel(self) -> int:
        """
        get_channel()

        Get current selected Channel

        returns: int
        """

        response = self.query_resource("INST:NSEL?")
        return int(response)

    def set_state(self, state: bool, channel: int = None) -> None:
        """
        set_state(state, channel)

        Enables/disables the output of the supply

        Args:
            state (bool): Supply state (True == enabled, False == disabled)
            channel (int): Index of the channel to control. valid options
                are 1-3
        """

        self._update_channel(channel)
        self.write_resource(f"CHAN:OUTP {1 if state else 0}")

    def get_state(self, channel: int = None) -> bool:
        """
        get_state(channel)

        Retrieve the current state of the output of the supply.

        Args:
            channel (int): index of the channel to control. Valid options
                are 1-3

        Returns:
            bool: Supply state (True == enabled, False == disabled)
        """

        self._update_channel(channel)
        response = self.query_resource("CHAN:OUTP?")
        if response not in ("ON", "1"):
            return False
        return True

    def on(self, channel: int = None) -> None:
        """
        on(channel)

        Enables the relay for the power supply's output equivalent to
        set_state(True).

        Args:
            channel (int): Index of the channel to control. Valid options
                are 1-3
        """

        self.set_state(True, channel)

    def off(self, channel: int = None) -> None:
        """
        off(channel)

        Disables the relay for the power supply's output equivalent to
        set_state(False).

        Args:
            channel (int): Index of the channel to control. Valid options
                are 1-3
        """

        self.set_state(False, channel)

    def toggle(self, channel: int = None) -> None:
        """
        toggle(channel)

        Reverses the current state of the Supply's output

        Args:
            channel (int): Index of the channel to control. Valid options
                are 1-3
        """

        self.set_state(self.get_state() ^ True, channel)

    def set_voltage(self, voltage: float, channel: int = None) -> None:
        """
        set_voltage(voltage)

        voltage: float or int, amplitude to set output to in Vdc

        channel: int=None, the index of the channel to set.
        Valid options are 1-3

        set the output voltage set point of channel "channel" specified by
        "voltage"
        """

        self._update_channel(channel)
        self.write_resource(f"SOUR:VOLT {voltage}")

    def get_voltage(self, channel: int = None) -> float:
        """
        get_voltage()

        channel: int=None, the index of the channel to set.
        Valid options are 1-3

        gets the output voltage set point in Vdc

        returns: float
        """

        self._update_channel(channel)
        response = self.query_resource("SOUR:VOLT?")
        return float(response)

    def set_current(self, current: float, channel: int = None) -> None:
        """
        set_current(current)

        current: float/int, current limit set point in Adc

        channel: int=None, the index of the channel to set.
        Valid options are 1-3

        sets the current limit setting for the power supply in Adc
        """

        self._update_channel(channel)
        self.write_resource(f"SOUR:CURR {current}")

    def get_current(self, channel: int = None) -> float:
        """
        get_current()

        channel: int=None, the index of the channel to set.
        Valid options are 1-3

        gets the current limit setting for the power supply in Adc

        returns: float
        """

        self._update_channel(channel)
        response = self.query_resource("SOUR:CURR?")
        return float(response)

    def measure_voltage(self, channel: int = None) -> float:
        """
        measure_voltage()

        returns measurement of the output voltage of the specified channel in
        Vdc.

        returns: float
        """

        self._update_channel(channel)
        response = self.query_resource("MEAS:VOLT?")
        return float(response)

    def measure_current(self, channel: int = None) -> float:
        """
        measure_current()

        returns measurement of the output current of the specified channel in
        Adc.

        returns: float
        """

        self._update_channel(channel)
        response = self.query_resource("MEAS:CURR?")
        return float(response)

    def all_on(self) -> None:
        """
        all_on()

        Enables the relay for ALL the power supply's outputs.

        """

        self.write_resource(f"OUTP {1}")

    def all_off(self) -> None:
        """
        all_off()

        Disables the relay for ALL the power supply's outputs.

        """

        self.write_resource(f"OUTP {0}")

    def all_toggle(self) -> None:
        """
        all_toggle()

        Reverses the current state of ALL the Supply's outputs.
        Performs a Read State Write State.

        """
        response = self.query_resource("OUTPut:STATe:ALL?")
        all_state = response not in ("ON", "1")
        self.write_resource(f"OUTP {all_state ^ True}")

    def pop_error_queue(self) -> Union[str, None]:
        """
        pop_error_queue()

        Retrieves a summary information of the error at the front of the error
        queue (FIFO). Information consists of an error number and some
        descriptive text. If the error queue is empty this function returns
        None. To clear the queue either repeatedly pop elements off the queue
        until it is empty or call the self.clear_status() method.

        Returns:
            Union[str, None]: Error summary information for the first item in
                the error queue or None if the queue is empty.
        """

        response = self.query_resource("SYST:ERR?")
        if response[0] == "0":
            return None
        return response.strip()

    def error_queue(self) -> List[str]:
        """
        error_queue()

        Retrieves the summary information for all errors currently in the error
        queue (FIFO), clearing it in the process. Information for each error
        consists of an error number and some descriptive text. If the error
        queue is empty this function returns an empty list.

        Returns:
            Union[str, None]: Error summary information for the first item in
                the error queue or None if the queue is empty.
        Returns:
            List: a list of error summary information for the errors in the
                error queue. Ordered by occurrence.
        """

        queue = []
        while True:
            error = self.pop_error_queue()
            if error is None:
                break
            queue.append(error)

        return queue