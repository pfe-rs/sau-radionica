import sys
from math import sin
import matplotlib.pyplot as plt

sys.path.append('../..')

from hw.sau_api.api_dryer import Dryer

# Set port name
PORT = '/dev/ttyUSB0'


class TestDryer(Dryer):

	def __init__(self, port):
		Dryer.__init__(self, port=port)

		# inicijalizovanje stanja
		self.dt = 0
		self.measurements = []
		self.controls = []

	def control(self, measurement):

		# dodajte vas kod ovde!
		# control treba da vraca int u rasponu [0,4000]
		self.dt += 1
		control_out = int(2000*(1+sin(self.dt * 0.01)))
		# end vas kod

		# real time plot, Marjanovic TM
		print("{} {}".format(measurement, control_out))
		for i in range(int(measurement/10)):
			print(" ", end="")
		print("*")
		for i in range(int(control_out/100)):
			print(" ", end="")
		print("O")

		# fill in the real plot
		self.measurements.append(measurement)
		self.controls.append(control_out)

		return control_out


tst = TestDryer(port=PORT)
tst.control_loop()

plt.plot(tst.measurements)
plt.plot(tst.controls)
plt.show()
