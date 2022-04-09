import sys
sys.path.append("../..")
from SauLib.API.api_BnBlaser import BnBlaser
from math import sin
import matplotlib.pyplot as plt

PORT = "/dev/ttyACM0"

t_sample = 0.5


class Test(BnBlaser):

    def __init__(self, port):
        BnBlaser.__init__(self, port=port)

        # inicijalizovanje stanja
        self.dt = 0
        self.measurements = []
        self.controls = []

    def control(self, measurement):

        # dodajte vas kod ovde!
        # control treba da vraca int u rasponu [-127, 128]
        self.dt += 1
        control_out = int(80*sin(self.dt * 0.1))
        # end vas kod

        # real time plot, Marjanovic TM
        print("{} {}".format(measurement, control_out))
        for i in range(int(measurement/10)):
            print(" ", end="")
        print("*")
        for i in range(int((120+control_out)/10)):
            print(" ", end="")
        print("O")

        # fill in the real plot
        self.measurements.append(measurement)
        self.controls.append(control_out)

        return control_out


test = Test(port=PORT)
test.control_loop()

plt.plot(test.measurements)
plt.plot(test.controls)
plt.show()
