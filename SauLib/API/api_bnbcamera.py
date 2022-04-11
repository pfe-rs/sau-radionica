import sys
import multiprocessing as mp
from turtle import position

sys.path.append('.')
from SauLib.devices.device import Device
from .api_base import ApiBase

import cv2
import numpy as np

ser = None
cap = None
width, height = None, None
x, y = None, None
mid_angle = 512
min_angle = mid_angle - 100
max_angle = mid_angle + 100

def init(cam):
    global cap, x, y, width, height
    cap = cv2.VideoCapture(cam)
    ret, frame = cap.read()

    height, width = frame[:, :, 0].shape
    x, y = np.meshgrid(np.linspace(0, width - 1, width),
                       np.linspace(0, height - 1, height))

def get_position():
    global cap, width, height, x, y

    ret, frame = cap.read()

    Kr, Kg, Kb = 0.6, 0.2, -0.9
    greenery = Kr * frame[:, :, 2] + Kg * frame[:, :, 1] + Kb * frame[:, :, 0]
    
    binarized = (greenery > 60) * 1.0

    x_sum = int(np.sum(x * binarized))
    y_sum = int(np.sum(y * binarized))
    n_sum = int(np.sum(binarized))

    if n_sum < 50:
        pos = 0, 0
    else:
        pos = (x_sum // n_sum, y_sum // n_sum)
        x_pos, y_pos = pos

    # cv2.imshow('frame', frame / 256 + np.stack([binarized, binarized, binarized], 2))
    cv2.imshow('frame', binarized)
    if (n_sum < 50):
        cv2.putText(frame, "Where is the ball?",
                    (height // 2, width // 2 - 40), cv2.FONT_HERSHEY_PLAIN, 1,
                    (255, 255, 255))
    else:
        cv2.circle(frame, pos, 5, (255, 255, 255))
        cv2.line(frame, pos, (x_sum // n_sum + 40, y_sum // n_sum + 40),
                 (255, 255, 255))
        cv2.putText(frame, "Here it is!",
                    (x_sum // n_sum + 40, y_sum // n_sum + 40),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
        cv2.line(frame, (width // 2, 0), (width // 2, height), (255, 255, 255))
    cv2.imshow('frame', frame)
    return pos


class CameraSensor(Device):
	
	def __init__(self, cam):
		init(cam)

	def get_data(self):
		return get_position()

class Motor(Device):
	
	def __init__(self, port, chan_id, motor_id, sleep=0.04):
		self.port = port
		self.sleep = sleep
		self.chan_id = chan_id
		BIND = 253
		OUT = 251
		CHAN_ID = chan_id
		INPUT_SRC = motor_id
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

class BallControl(Device):

	def __init__(self, port, sleep=0.04, verbosity=False):
		self.sleep = sleep
		self.position_x = mp.Value('d', 0.0)
		self.position_y = mp.Value('d', 0.0)
		self.camera_process = mp.Process(target=self.camera_loop)
		Device.__init__(self, channel=5, port=port, verbosity=verbosity)
		self.motor = Motor(
			port=self.port,
			chan_id=6,
			motor_id=1,
			sleep=self.sleep
		)

		self.camera_process.start()
		self.camera_sensor = None

	def camera_loop(self):
		self.camera_sensor = CameraSensor(cam=0)
		while True:
			position = self.camera_sensor.get_data()
			keypressed = cv2.waitKey(30)
			if keypressed == ord('q'):
				break
			self.position_x.value = position[0]
			self.position_y.value = position[1]

	def get_data(self):
		return self.position_x.value, self.position_y.value

	def send_data(self, command):
		self.motor.send_data(command)


class BallAndBeamCamera(ApiBase):
	def __init__(self, port=None, verbosity= False):
		ApiBase.__init__(self)
		self.ball = BallControl(port=port, verbosity=verbosity)

	def write_actuator(self, command):
		self.ball.send_data(command)

	def read_sensor_data(self):
		return self.ball.get_data()

	def exit(self):
		print("ocu da ga ubijem")
		self.ball.camera_process.terminate()
