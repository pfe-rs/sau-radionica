import sys
from math import sin
import matplotlib.pyplot as plt
sys.path.append('../..')
from SauLib.API.api_dryer import Dryer

class TestDryer(Dryer):

	def __init__(self):
		Dryer.__init__(self)

		# Inicijalizacija stanja
		self.dt = 0
		self.measurements = []
		self.controls = []

	def control(self, measurement):

		# Dodajte vaš kod ovde!
		# control treba da vraća int u rasponu [0,255]
		self.dt += 1
		control_out = int(100*(1+sin(self.dt * 0.01)))
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


tst = TestDryer()
tst.control_loop()

plt.plot(tst.measurements)
plt.plot(tst.controls)
plt.show()
