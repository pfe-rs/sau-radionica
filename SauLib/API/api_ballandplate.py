import sys
import multiprocessing as mp

sys.path.append('.')
from SauLib.devices.device import Device
from .api_base import ApiBase

import cv2
import numpy as np

cap = None


def init(cam):
    global cap
    cap = cv2.VideoCapture(cam)


def get():
    global cap
    ret, frame = cap.read()

    b, g, r = cv2.split(frame)

    processed = 1.0 * r + 0.5 * g - 1.5 * b
    rect, thresh = cv2.threshold(processed, 50, 255, 0)

    M = cv2.moments(thresh)

    cX = 0
    cY = 0

    if M['m00'] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(frame, "loptica", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    black = cv2.inRange(hsv, (0, 0, 0), (255, 120, 90))

    indencies = np.where(black == 255)

    ymin = np.amin(indencies[0])
    ymax = np.amax(indencies[0])

    xmin = np.amin(indencies[1])
    xmax = np.amax(indencies[1])

    plate_cx = xmin + (xmax - xmin) / 2
    plate_cy = ymin + (ymax - ymin) / 2

    x_pos = cX - plate_cx
    y_pos = plate_cy - cY

    print("lib vraca {}".format((x_pos, y_pos)))

    return [x_pos, y_pos]



class CameraSensor(Device):
	
	def __init__(self, cam):
		init(cam)

	def get_data(self):
		data = get()
		
		x_pos = data[0]
		y_pos = data[1]

		return x_pos, y_pos


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
		self.motor1 = Motor(
			port=self.port,
			chan_id=9,
			motor_id=1,
			sleep=self.sleep
		)
		self.motor2 = Motor(
			port=self.port,
			chan_id=10,
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
