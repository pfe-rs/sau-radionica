import serial
import logging
import time
import serial.tools.list_ports

class Port:
    def __init__(self, port: str, baudrate: int = 19200, timeout: int = 1, verbosity: bool = False):
        """
        Initialize serial port
        :param port: string containing port name
        :param baudrate:
        :param timeout:
        :param verbosity:
        """
        if not port:
            # Raise exception if port is not defined
            raise Exception(
                'Port should be defined!'
            )
        available_devices = [
            i.device for i in list(serial.tools.list_ports.comports())
        ]
        if port not in available_devices:
            raise Exception(
                'Requested port is not available'
            )
        self.logger = None
        if verbosity:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
        self.log('Port init started ')
        self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
        )
        self.log('Port init completed ')

    def send(self, data: list, sleep: float = 0.02) -> list:
        """
        Send data package to the designed port
        :param data: list of data points
        :param sleep: time to wait between write and read methods in seconds
        :return: list of integers
        """
        self.log('Sending data started ')
        self.ser.write(bytearray(data))
        time.sleep(sleep)
        rsp = self.ser.read_all()
        self.log('Sending data completed, received {0} '.format(list(rsp)))
        return list(rsp)

    def read(self):
        """
        Read all bytes currently available in the buffer of the OS.
        :return: list of integers
        """
        self.log('Reading data started ')
        rsp = self.ser.read_all()
        self.log('Reading data completed, received {}'.format(list(rsp)))
        return list(rsp)

    def log(self, message: str):
        if self.logger is not None:
            self.logger.info(message)
