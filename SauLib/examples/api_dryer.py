from hw.Devices import device
from hw.sau_api.api_base import ApiBase


class TempSensor(device.Device):

    def __init__(self, port, sleep: float = 0.04):
        self.port = port
        self.sleep = sleep  # Time to sleep between write and read procedures
        # Bind Sensor to Channel
        BIND = 253  # Binding signal
        IN = 252  # Input signal
        CHAN_ID = 2  # Channel ID
        INPUT_PARAM = 3  # Input Parameter
        INPUT_SRC = 0  # Input source 0 - ADC
        sensor_init = self.port.send(
            [BIND, IN, CHAN_ID, INPUT_PARAM, INPUT_SRC],
            self.sleep
        )
        if sensor_init[0] != 65:
            raise Exception(
                'Failed temperature sensor binding!'
            )

    def get_data(self):
        SENSOR = 255
        CHAN_ID = 2  # Channel ID
        data_rsp = list(self.port.send(
            [SENSOR, CHAN_ID],
            self.sleep)
        )
        if len(data_rsp) == 3:
            temperature = data_rsp[1] + data_rsp[2]*2**8
        else:
            raise Exception(
                'Measurement Error!'
            )
        return temperature


class Heater(device.Device):

    def __init__(self, port, sleep: float = 0.04):
        self.port = port
        self.sleep = sleep
        # Bind Heater to Channel
        BIND = 253  # Binding signal
        OUT = 251  # Output signal
        CHAN_ID = 2  # Channel ID
        INPUT_SRC = 0  # Input source 0 - ADC
        heater_init = self.port.send(
            [BIND, OUT, CHAN_ID, INPUT_SRC],
            self.sleep
        )
        if heater_init[0] != 65:
            raise Exception(
                'Failed actuator binding!'
            )

    def send_data(self, temperature: int):
        high = temperature//256  # High Byte
        low = temperature % 256  # Low Byte
        ACT = 254
        CHAN_ID = 2  # Channel ID

        rsp = self.port.send(
            [ACT, CHAN_ID, high, low],
            self.sleep
        )
        if rsp[0] != 65:
            raise Exception(
                'Failed actuator write!'
            )


class DryerControll(device.Device):

    def __init__(self, port, sleep: float = 0.04, verbosity: bool = False):
        self.sleep = sleep
        device.Device.__init__(self, port=port, verbosity=verbosity)
        # Init Sensor
        self.temp_sensor = TempSensor(port=self.port, sleep=self.sleep)
        # Init Actuator
        self.heater = Heater(port=self.port, sleep=self.sleep)

    def send_data(self, temperature: int):
        self.heater.send_data(temperature)

    def get_data(self):
        temp = self.temp_sensor.get_data()
        return temp


class Dryer(ApiBase):

    def __init__(self, port: str, verbosity: bool = False):
        ApiBase.__init__(self)
        # Dryer init
        self.dryer = DryerControll(port=port, verbosity=verbosity)

    def write_actuator(self, command):
        self.dryer.send_data(command)

    def read_sensor_data(self):
        return self.dryer.get_data()
