import sys

sys.path.append('../..')
from SauLib.API.api_ballandplate import BallAndPlate

# PORT = '/dev/ttyACM0'


import sys
from math import sin, cos
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

		self.dt += 1
		MIN_SERVO = 30
		MAX_SERVO = 150

##### POCETAK VASEG KODA
		# funkcija treba da vrati signal kontrole, a dobija signal senzora kao ulaz

		# sinusi koji talasaju [0,1] kao primer
		control_x = (1+sin(self.dt * 0.01))/2
		control_y = (1+cos(self.dt * 0.01))/2

		#control_outx = (96+dt) % 200
		#control_outy = 96

###### KRAJ VASEG KODA

		control_x_clamped = int(MIN_SERVO + (MAX_SERVO-MIN_SERVO) * control_x)
		control_y_clamped = int(MIN_SERVO + (MAX_SERVO-MIN_SERVO) * control_y)

		print("Measurement {}".format(measurement))
		print("Control {} {}".format(control_x_clamped, control_y_clamped))

		# fill in the real plot
		self.measurements.append(measurement)
		self.controls.append((control_x_clamped, control_y_clamped))

		return control_x_clamped, control_y_clamped


tst = TestBnP(port=PORT)
tst.control_loop()

plt.plot(tst.measurements)
plt.plot(tst.controls)
plt.show()
