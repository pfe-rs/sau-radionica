import sys

sys.path.append('../..')
from SauLib.API.api_ballandplate import BallAndPlate

# PORT = '/dev/ttyACM0'

# diskusija = BallAndPlate(PORT)
# while True:
# 	diskusija.write_actuator(1,150)
# 	diskusija.write_actuator(1,120)
# 	diskusija.write_actuator(2,138)
# 	print(diskusija.read_sensor_data())

import sys
from math import sin
import matplotlib.pyplot as plt

sys.path.append('../..')


# Set port name
PORT = '/dev/ttyACM0'


class TestBnP(BallAndPlate):

	def __init__(self, port):
		BallAndPlate.__init__(self,port=port)

		# inicijalizovanje stanja
		self.dt = 0
		self.measurements = []
		self.controls = []

	def control(self, measurement):

		# dodajte vas kod ovde!
		# control treba da vraca int u rasponu [0,4000]
		self.dt += 1
		control_outx = int(255//2*(1+sin(self.dt * 0.01)))
		control_outy = int(255//2*(1+sin(self.dt * 0.01)))
		# end vas kod

		print("Measurement {}".format(measurement))
		print("Control {} {}".format(control_outx, control_outy))

		# real time plot, Marjanovic TM
		# print("{} {}".format(measurement, control_out))
		# for i in range(int(measurement/10)):
		# 	print(" ", end="")
		# print("*")
		# for i in range(int(control_outx/100)):
		# 	print(" ", end="")
		# print("O")

		# fill in the real plot
		# self.measurements.append(measurement)
		# self.controls.append(control_out)

		return control_outx, control_outy


tst = TestBnP(port=PORT)
tst.control_loop()

plt.plot(tst.measurements)
plt.plot(tst.controls)
plt.show()
