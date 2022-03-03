from typing import Sequence
from pythonequipmentdrivers import Scpi_Instrument, VisaIOError
import numpy as np


class Agilent_33250A(Scpi_Instrument):
    """
    Agilent_33250A(address)

    address : str, address of the connected function generator

    object for accessing basic functionallity of the Agilent_33250A function
    generator
    """

    valid_wave_types = ('SIN', 'SQU', 'RAMP', 'PULS', 'NOIS', 'DC', 'USER')

    def set_output_state(self, state: bool) -> None:
        self.instrument.write(f"OUTP {1 if state else 0}")

    def get_output_state(self) -> bool:
        response = self.instrument.query("OUTP?")
        return bool(int(response))

    def set_output_impedance(self, impedance) -> None:
        """
        Valid options are 1-10k, min, max, and inf
        """

        valid_str = ('MIN', 'MAX', 'INF')

        if isinstance(impedance, (float, int)):
            z = np.clip(impedance, 10, 10e3)
            self.instrument.write(f'OUTP:LOAD {z}')
        elif isinstance(impedance, str) and (impedance.upper() in valid_str):
            self.instrument.write(f'OUTP:LOAD {impedance.upper()}')

    def get_output_impedance(self) -> float:
        response = self.instrument.query('OUTP:LOAD?')
        return float(response)

    def set_output_polarity(self, polarity: bool = True) -> None:
        """set_output_polarity()
        Invert the waveform relative to the offset voltage. In the normal mode
        (default), the waveform goes positive during the first part of the
        cycle. In the inverted mode, the waveform goes negative during the
        first part of the cycle.

        Args:
            polarity (bool, optional): True == Normal, False == Inverted.
            Defaults to True.
        """
        self.instrument.write(f"OUTP:POL {'NORM' if polarity else 'INV'}")

    def get_output_polarity(self) -> bool:
        response = self.instrument.query("OUTP:POL?")
        if response == 'NORM':
            return True
        elif response == 'INV':
            return False

    def set_waveform_type(self, waveform: str) -> None:

        wave = str(waveform).upper()[0:4]

        if (wave in self.valid_wave_types):
            self.instrument.write(f'FUNC {wave}')
        else:
            raise ValueError('Invalide Waveform type. '
                             f'Supported: {self.valid_wave_types}')

    def get_waveform_type(self) -> str:
        response = self.instrument.query('FUNC?')
        wave = response.strip()
        return wave.upper()

    def get_voltage_units(self) -> str:
        return self.instrument.query('VOLT:UNIT?')

    def set_voltage_units(self, units: str = 'VPP') -> None:
        """
        Valid options are VPP, VRMS, DBM
        """

        valid_str = ('VPP', 'VRMS', 'DBM')

        if isinstance(units, str) and (units.upper() in valid_str):
            self.instrument.write(f'VOLT:UNIT {units.upper()}')

    def set_voltage_amplitude(self, voltage: float) -> None:
        self.instrument.write(f'VOLT {float(voltage)}')

    def get_voltage_amplitude(self) -> float:
        response = self.instrument.query('VOLT?')
        return float(response)

    def set_voltage_offset(self, voltage: float) -> None:
        self.instrument.write(f'VOLT:OFFS {float(voltage)}')

    def get_voltage_offset(self) -> float:
        response = self.instrument.query('VOLT:OFFS?')
        return float(response)

    def set_voltage_high(self, voltage: float) -> None:
        self.instrument.write(f'VOLT:HIGH {float(voltage)}')

    def get_voltage_high(self) -> float:
        response = self.instrument.query('VOLT:HIGH?')
        return float(response)

    def set_voltage_low(self, voltage: float) -> None:
        self.instrument.write(f'VOLT:LOW {float(voltage)}')

    def get_voltage_low(self) -> float:
        response = self.instrument.query('VOLT:LOW?')
        return float(response)

    def set_frequency(self, frequency: float) -> None:
        self.instrument.write(f'FREQ {float(frequency)}')

    def get_frequency(self) -> float:
        response = self.instrument.query('FREQ?')
        return float(response)

    def set_voltage_auto_range(self, state: bool) -> None:
        self.instrument.write(f"VOLT:RANG:AUTO {'ON' if state else 'OFF'}")

    def get_voltage_auto_range(self) -> bool:
        response = self.instrument.query('VOLT:RANG:AUTO?')
        if '1' in response:
            return True
        return False

    def set_voltage_auto_range_once(self) -> None:
        self.instrument.write("VOLT:RANG:AUTO ONCE")

    def set_burst_state(self, state: bool) -> None:
        self.instrument.write('BURS:STAT {}'.format(1 if state else 0))

    def set_pulse_period(self, period: float) -> None:
        self.instrument.write(f'PULSE:PER {float(period)}')

    def get_pulse_period(self):
        response = self.instrument.query('PULSE:PER?')
        return float(response)

    def set_pulse_width(self, width) -> None:
        self.instrument.write(f'PULSE:WIDT {float(width)}')

    def get_pulse_width(self) -> float:
        response = self.instrument.query('PULSE:WIDT?')
        return float(response)

    def set_square_duty_cycle(self, dc) -> None:
        self.instrument.write(f'FUNC:SQU:DCYCLE {float(dc)}')

    def get_square_duty_cycle(self) -> float:
        response = self.instrument.query('FUNC:SQU:DCYCLE?')
        return float(response)

    def get_burst_state(self, source: int = 1) -> bool:
        response = self.instrument.query(f'SOUR{int(source)}:BURS:STAT?')
        return bool(int(response))

    def set_burst_mode(self, mode: str) -> None:
        mode = mode.upper()
        burst_modes = ('TRIG', 'GAT')
        if mode not in burst_modes:
            raise ValueError(f'Invalid mode, valid modes are: {burst_modes}')
        self.instrument.write(f'BURS:MODE {mode}')

    def get_burst_mode(self) -> str:
        response = self.instrument.query('BURS:MODE?')
        return response.strip().lower()

    def set_burst_ncycles(self, ncycles: int) -> None:
        str_options = ['INF', 'MIN', 'MAX']
        if isinstance(ncycles, int):
            self.instrument.write(f'BURS:NCYC {ncycles}')
        elif isinstance(ncycles, str) and (ncycles.upper() in str_options):
            self.instrument.write(f'BURS:NCYC {ncycles.upper()}')
        else:
            raise ValueError('invalid entry for ncycles')

    def get_burst_ncycles(self):
        response = self.instrument.query('BURS:NCYC?')
        return int(float(response))

    def trigger(self) -> None:
        self.instrument.write('TRIG')

    def store_arbitrary_waveform(self, data: Sequence,
                                 arb_name: str='VOLATILE',
                                 clear: bool = True) -> None:

        if not (8 < len(data) < 65536):
            raise ValueError('data must be between 8 and 65536 samples')

        data = np.array(data)
        # normalize the data:
        data = (data - np.min(data)) / (np.max(data) - np.min(data))
        data *= 2047  # spans +/- 2047 in the 33250
        data = data.astype(int)

        timeout_old = self.timeout
        self.timeout = 4000  # big waveforms need more time

        cmd_str = "DATA:DAC"
        try:
            self.instrument.write('{} {},{}'.format(cmd_str,
                                                    'VOLATILE',
                                                    ",".join(map(str, data))))
        except VisaIOError:
            print(f'timeout {self.timeout} trying 2x')
            self.timeout = self.timeout * 2
            self.instrument.write('{} {},{}'.format(cmd_str,
                                                    'VOLATILE',
                                                    ",".join(map(str, data))))
        self.timeout = timeout_old

        if clear:
            self.instrument.write(f'DATA:DEL {arb_name}')
        # send data
        if arb_name != 'VOLATILE':
            self.instrument.write(f'DATA:COPY {arb_name}')
        return

    def select_arbitrary_waveform(self, arb_name: str='VOLATILE') -> None:
        self.instrument.write(f'FUNC:USER {arb_name}')
        self.set_waveform_type('USER')
        return

    def set_sample_rate(self, sample_rate: float) -> None:
        self.instrument.write(f'APPLY:USER {sample_rate}')
        return
