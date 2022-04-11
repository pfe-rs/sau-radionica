import matplotlib.pyplot as plt
from math import sin
import sys

sys.path.append('../..')
from SauLib.API.api_bnbcamera import BallAndBeamCamera

class TestBnBCamera(BallAndBeamCamera):

	def __init__(self):
		BallAndBeamCamera.__init__(self)

		# inicijalizovanje stanja
		self.dt = 0
		self.measurements = []
		self.controls = []

	def control(self, measurement):

		self.dt += 1
		MIN_SERVO = 70
		MAX_SERVO = 110


# POCETAK VASEG KODA
		# funkcija treba da vrati signal kontrole, a dobija signal senzora kao ulaz

		# sinusi koji talasaju [0,1] kao primer
		control_x = (1+sin(self.dt * 0.01))/2

# KRAJ VASEG KODA

		control_x_clamped = int(MIN_SERVO + (MAX_SERVO-MIN_SERVO) * control_x)

		print("Measurement {}".format(measurement))
		print("Control {}".format(control_x_clamped))

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
		self.controls.append(control_x_clamped)

		return control_x_clamped


tst = TestBnBCamera()
tst.control_loop()

plt.plot(tst.measurements)
plt.plot(tst.controls)
plt.show()
