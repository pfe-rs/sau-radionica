import time
import signal


class ApiBase:

	def __init__(self):
		self.start_time = 0
		self.sample_period = 0.02
		self.running = True
		signal.signal(signal.SIGINT, self.exit_gracefully)

	def read_sensor_data(self):
		return None

	def control(self, measurement):
		return None  # <-- Actuator commands

	def write_actuator(self, command):
		pass

	def exit_gracefully(self, signum, frame):
		self.running = False
		self.exit()

	def control_loop(self):
		self.start_time = time.time() + self.sample_period
		while self.running:
			while time.time() < self.start_time:
				pass
			self.start_time += self.sample_period

			measurement = self.read_sensor_data()
			command = self.control(measurement)
			self.write_actuator(command)
