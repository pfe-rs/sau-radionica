import matplotlib.pyplot as plt
from math import sin
import sys

sys.path.append('../..')
from SauLib.API.api_ballandtube import BallAndTube

# Set port name
PORT = '/dev/ttyACM0'

class TestBnBCamera(BallAndTube):

    def __init__(self, port):
        BallAndTube.__init__(self, port=port)

        # inicijalizovanje stanja
        self.dt = 0
        self.measurements = []
        self.controls = []

    def control(self, measurement):

        self.dt += 1
        MIN_FAN = 0
        MAX_FAN = 255

# POCETAK VASEG KODA
        # funkcija treba da vrati signal kontrole, a dobija signal senzora kao ulaz

        # sinusi koji talasaju [0,1] kao primer
        control = (1+sin(self.dt * 0.01))/2

# KRAJ VASEG KODA

        control = max(control, 0)
        control = min(control, 1)

        control_clamped = int(MIN_FAN + (MAX_FAN-MIN_FAN) * control)

        print("Measurement {}".format(measurement))
        print("Control {}".format(control_clamped))

        # real time plot, Marjanovic TM
        # print("{} {}".format(measurement, control_out))
        # for i in range(int(measurement/10)):
        # 	print(" ", end="")
        # print("*")
        # for i in range(int(control_out/100)):
        # 	print(" ", end="")
        # print("O")

        # fill in the real plot
        self.measurements.append(measurement)
        self.controls.append(control_clamped)

        return control_clamped


tst = TestBnBCamera(port=PORT)
tst.control_loop()

plt.plot(tst.measurements)
plt.plot(tst.controls)
plt.show()


h = Heater(PORT)
