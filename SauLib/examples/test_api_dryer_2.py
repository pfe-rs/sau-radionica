import sys
from time import sleep
from SauLib.API.api_dryer import Dryer

class TestDryer(Dryer):

	def __init__(self):
		Dryer.__init__(self, verbosity=True)
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


tst = TestDryer()
tst.control_loop()
