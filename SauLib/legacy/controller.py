from api_bnb_dynamixel import ApiBnbDynamixel as Api
import time


class MyController(Api):

	def __init__(self, camera_port=0, motor_port='/dev/ttyUSB0'):
		Api.__init__(self, camera_port, motor_port)
		self.state = [0, 0]
		self.Kp = 1
		self.Ki = 0
		self.Kd = 1
		self.reference = 320

	def control(self, measurement):

		if measurement is None or measurement == 0:
			measurement = self.state[0]

		print("Measurement: " + str(measurement))
		for i in range(int((measurement-250)/3)):
			print(" ", end='')
		print('*')

		e = (measurement - self.reference)

		Kp, Ki, Kd = 0.05, 0.0001, 0.5

		P = Kp * e
		I = Ki * self.state[1]
		D = Kd * (measurement - self.state[0])

		self.state = [measurement, self.state[1] + e]

		# print("PID:         " + str(512 + P + I + D))

		return 512 + P + I + D


if __name__ == "__main__":
	A = MyController(camera_port=0)
	A.control_loop()
