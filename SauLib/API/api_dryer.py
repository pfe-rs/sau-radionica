from SauLib.devices.device import Device, InputSource, OutputSource
from .api_base import ApiBase

TEMP_SENSOR_TEMPERATURE_BYTES = 2

class TempSensor(Device):

    def __init__(self, port, sleep: float = 0.04):
        Device.__init__(self, port, channel=2, sleep=sleep)
        self.bind_input_device(InputSource.ADC, 11)

    def get_data(self):
        return self.sensor()

class Heater(Device):

    def __init__(self, port, sleep: float = 0.04):
        Device.__init__(self, channel=2, port=port, sleep=sleep)
        self.bind_output_device(OutputSource.DAC)

    def send_data(self, temperature: int):
        self.actuate(temperature, TEMP_SENSOR_TEMPERATURE_BYTES)

class DryerControl(Device):

    def __init__(self, port, sleep: float = 0.04, verbosity: bool = False):
        Device.__init__(self, channel=2, port=port, verbosity=verbosity, sleep=sleep)
        self.temp_sensor = TempSensor(port=self.port, sleep=self.sleep)
        self.heater = Heater(port=self.port, sleep=self.sleep)

    def send_data(self, temperature: int):
        self.heater.send_data(temperature)

    def get_data(self):
        temp = self.temp_sensor.get_data()
        return temp


class Dryer(ApiBase):

    def __init__(self, port: str, verbosity: bool = False, sleep: float = 0.04):
        ApiBase.__init__(self)
        self.dryer = DryerControl(port=port, sleep=sleep, verbosity=verbosity)

    def write_actuator(self, command):
        self.dryer.send_data(command)

    def read_sensor_data(self):
        return self.dryer.get_data()
