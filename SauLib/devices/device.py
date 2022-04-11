from enum import IntEnum
from typing import Union
from .port import Port
import serial

class UMAKConstants:
    CMD_SENSOR = 255
    CMD_ACT = 254
    CMD_BIND = 253
    BIND_IN = 252
    BIND_OUT = 251
    ACKNOWLEDGE = ord('A')
    ERROR = ord('E')
    SENSOR = ord('S')

class InputSource(IntEnum):
    ADC = 0
    TEMP_SENSOR = 1

class OutputSource(IntEnum):
    DAC = 0
    PWM1 = 1
    PWM2 = 2

class Device:

    def __init__(self, channel: int, port: Union[str, Port, None] = None, baudrate: int = 19200, timeout: int = 1, verbosity: bool = False, sleep: float = 0.04):
        """
        Initialize serial port
        :param port: port name
        :param baudrate: baudrate integer
        :param timeout:
        :param verbosity:
        """
        if port is None:
            all_ports = [i.device for i in list(serial.tools.list_ports.comports())]
            if len(all_ports) == 0:
                raise Exception('No open ports! Please make sure the microcontroller is connected.')
            self.port = Port(
                port=all_ports[0],
                baudrate=baudrate,
                timeout=timeout,
                verbosity=verbosity
            )
        elif isinstance(port, Port):
            self.port = port
        else:
            self.port = Port(
                port=port,
                baudrate=baudrate,
                timeout=timeout,
                verbosity=verbosity
            )
        self.channel: int = channel
        self.sleep: float = sleep

    def init_device(self):
        pass

    def send_data(self, data):
        pass

    def get_data(self):
        pass

    def bind_input_device(self, source: InputSource, param: int):
        sensor_init = self.port.send(
            [UMAKConstants.CMD_BIND, UMAKConstants.BIND_IN, self.channel, param, int(source)],
            self.sleep
        )
        if sensor_init[0] != UMAKConstants.ACKNOWLEDGE:
            raise Exception('Failed input device binding!')

    def bind_output_device(self, source: OutputSource):
        actuator_init = self.port.send(
            [UMAKConstants.CMD_BIND, UMAKConstants.BIND_OUT, self.channel, int(source)],
            self.sleep
        )
        if actuator_init[0] != UMAKConstants.ACKNOWLEDGE:
            raise Exception('Failed output device binding!')

    def actuate(self, data: int, bytes: int):
        actuate_data = list(data.to_bytes(bytes, byteorder='big'))
        rsp = self.port.send(
            [UMAKConstants.CMD_ACT, self.channel] + actuate_data,
            self.sleep
        )
        if rsp[0] != UMAKConstants.ACKNOWLEDGE:
            raise Exception('Failed actuator write!')

    def sensor(self) -> int:
        data_rsp = self.port.send(
            [UMAKConstants.CMD_SENSOR, self.channel],
            self.sleep
        )
        sensor_data: int = 0
        if len(data_rsp) > 1 and data_rsp.pop(0) == UMAKConstants.SENSOR:
            while len(data_rsp) > 0:
                sensor_data <<= 8
                sensor_data += data_rsp.pop()
            return sensor_data
        else:
            raise Exception('Failed to read sensor data!')
