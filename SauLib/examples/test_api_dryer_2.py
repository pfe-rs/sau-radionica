import sys
from math import sin
import matplotlib.pyplot as plt
from time import sleep

sys.path.append('../..')

from SauLib.API.api_dryer import Dryer

# Set port name
PORT = '/dev/ttyACM0'


class TestDryer(Dryer):

	def __init__(self, port):
		Dryer.__init__(self, port=port, verbosity=True)
		while True:
			print('Writing 255')
			self.write_actuator(255)
			for i in range(10):
				sleep(1)
				print(self.read_sensor_data())
			print('Writing 0')
			self.write_actuator(0)
			for i in range(10):
				sleep(1)
				print(self.read_sensor_data())

	def control(self, measurement):
		#print(measurement)
		return 0


tst = TestDryer(port=PORT)
tst.control_loop()
