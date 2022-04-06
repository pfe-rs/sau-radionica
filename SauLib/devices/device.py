from filipid.port import Port


class Device:

    def __init__(self, port: str,  baudrate: int = 19200, timeout: int = 1, verbosity: bool = False):
        """
        Initialize serial port
        :param port: port name
        :param baudrate: baudrate integer
        :param timeout:
        :param verbosity:
        """
        self.port = Port(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
            verbosity=verbosity
        )

    def init_device(self):
        pass

    def send_data(self, data):
        pass

    def get_data(self):
        pass
