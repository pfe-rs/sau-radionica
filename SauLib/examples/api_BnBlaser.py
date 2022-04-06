import sys 
sys.path.append("..\\..")
from hw.Devices.device import *
from hw.sau_api.api_base import ApiBase


class Laser(Device):
    def __init__(self, port):
        self.port = port

        sensor_init = self.port.send([253, 252, 0, 0, 0])
        if sensor_init[0] != 65:
            raise Exception(
                'Sensor init failed'
            )

    def get_data(self):
        data_rsp = list(self.port.send([255, 0], 0.02))
        if len(data_rsp) == 3:
            position = data_rsp[1] + data_rsp[2]*2**8
        else:
            raise Exception(
                'Measurement Error!'
            )
        return position


class Beam(Device):
    def __init__(self, port):
        self.port = port

        # Bind Heater to Channel
        beam_init = self.port.send([253, 251, 1, 1], 0.02)
        if beam_init[0] != 65:
            raise Exception(
                'Failed actuator binding!'
            )

    def send_data(self, position: int):
        rsp = self.port.send([254, 1, position+127], 0.04)


class BnBLaserControll(Device):
    def __init__(self, port):
        Device.__init__(self, port=port)
        # Init Sensor
        self.position = Laser(port=self.port)
        # Init Actuator
        self.beam = Beam(port=self.port)

    def send_data(self, position: int):
        self.beam.send_data(position)

    def get_data(self):
        pos = self.position.get_data()
        return pos


class BnBlaser(ApiBase):
    def __init__(self, port: str):
        ApiBase.__init__(self)
        # Dryer init
        self.BnB = BnBLaserControll(port=port)

    def write_actuator(self, command):
        self.BnB.send_data(command)

    def read_sensor_data(self):
        return self.BnB.get_data()

    def exit(self):
        pass
