import sys 
sys.path.append("..\\..")
from hw.Devices.device import *
from hw.sau_api.api_base import ApiBase


class Thermistor(Device):
    def __init__(self, port):
        self.port = port

        sensor_init = self.port.send([253,252,0,0,0]);
        if sensor_init[0] != 65:
            raise Exception(
                'Sensor init failed'
            )

    def get_data(self):
        data_rsp = list(self.port.send([255, 0], 0.02))
        if len(data_rsp) == 3:
            temperature = data_rsp[1] + data_rsp[2]*2**8
        else:
            raise Exception(
                'Measurement Error!'
            )
        return temperature


class Heater(Device):

    def __init__(self, port):
        self.port = port

        # Bind Heater to Channel
        heater_init = self.port.send([253, 251, 1, 1], 0.02)
        if heater_init[0] != 65:
            raise Exception(
                'Failed actuator binding!'
            )

    def send_data(self, temperature: int):
        rsp = self.port.send([254, 1, 255-temperature], 0.04)


class DryerDiyControll(Device):
    def __init__(self, port, verbosity: bool = False):
        Device.__init__(self, port=port, verbosity = verbosity)
        # Init Sensor
        self.temp_sensor = Thermistor(port=self.port)
        # Init Actuator
        self.heater = Heater(port=self.port)

    def send_data(self, temperature: int):
        self.heater.send_data(temperature)

    def get_data(self):
        temp = self.temp_sensor.get_data()
        return temp


class DryerDiy(ApiBase):
    def __init__(self, port: str, verbosity: bool = False):
        ApiBase.__init__(self)
        # Dryer init
        self.dryer = DryerDiyControll(port=port, verbosity=verbosity)

    def write_actuator(self, command):
        self.dryer.send_data(command)

    def read_sensor_data(self):
        return self.dryer.get_data()
