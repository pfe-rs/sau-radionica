import sys
import multiprocessing as mp

sys.path.append('../..')
from hw.Devices import device
from hw.sau_api.api_base import ApiBase

sys.path.append('../ball_and_plate')

import lib


class CameraSensor(device.Device):
	
	def __init__(self, cam):
		lib.init(cam)

	def get_data(self):
		data = lib.get()
		
		x_pos = data[0]
		y_pos = data[1]

		return x_pos, y_pos


class Motor(device.Device):
	
	def __init__(self, port, chan_id, motor_id, sleep=0.04):
		self.port = port
		self.sleep = sleep
		self.chan_id = chan_id
		BIND = 253
		OUT = 251
		CHAN_ID = chan_id
		INPUT_SRC = motor_id + 2
		motor_init = self.port.send(
			[BIND, OUT, CHAN_ID, INPUT_SRC],
			self.sleep
		)
		if motor_init[0] != 65:
			raise Exception('Failed actuator binding!')

	def send_data(self, pos):
		mot_pos = pos
		ACT = 254
		CHAN_ID = self.chan_id

		ack = self.port.send([ACT, CHAN_ID, mot_pos])
		if ack[0] != 65:
			raise Exception('Failed actuator write!')


class BallControl(device.Device):

	def __init__(self, port, sleep=0.04, verbosity=False):
		self.sleep = sleep
		self.position_x = mp.Value('d', 0.0)
		self.position_y = mp.Value('d', 0.0)
		self.camera_process = mp.Process(target=self.camera_loop)
		device.Device.__init__(self, port=port, verbosity=verbosity)
		self.motor1 = Motor(
			port=self.port,
			chan_id=5,
			motor_id=1,
			sleep=self.sleep
		)
		self.motor2 = Motor(
			port=self.port,
			chan_id=6,
			motor_id=2,
			sleep=self.sleep
		)
		self.camera_process.start()
		self.camera_sensor = None

	def camera_loop(self):
		self.camera_sensor = CameraSensor(cam=0)
		while True:
			tmp_x, tmp_y = self.camera_sensor.get_data()

			self.position_x.value = tmp_x
			self.position_y.value = tmp_y

	def send_data(self, motor_id, command):
		if motor_id == 1:
			self.motor1.send_data(command)
		elif motor_id == 2:
			self.motor2.send_data(command)
		else:
			print('Bad motor ID: {}'.format(motor_id))

	def get_data(self):
		x_pos = self.position_x.value
		y_pos = self.position_y.value
		return x_pos, y_pos


class BallAndPlate(ApiBase):
	def __init__(self, port, verbosity= False):
		ApiBase.__init__(self)
		self.ball = BallControl(port=port, verbosity=verbosity)

	def write_actuator(self, command):
		command1, command2 = command
		self.ball.send_data(1, command1)
		self.ball.send_data(2, command2)

	def read_sensor_data(self):
		return self.ball.get_data()

	def exit(self):
		print("ocu da ga ubijem")
		self.ball.camera_process.terminate()		
