import sys
import multiprocessing as mp
from turtle import position

sys.path.append('.')
from SauLib.devices.device import Device, OutputSource
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
prev_pos = None

def init(cam):
    global cap, x, y, width, height
    cap = cv2.VideoCapture(cam)
    ret, frame = cap.read()

    height, width = frame[:, :, 0].shape
    x, y = np.meshgrid(np.linspace(0, width - 1, width),
                       np.linspace(0, height - 1, height))

def get_position():
    global cap, width, height, x, y, prev_pos

    ret, frame = cap.read()

    Kr, Kg, Kb = 0.6, 0.2, -0.9
    greenery = Kr * frame[:, :, 2] + Kg * frame[:, :, 1] + Kb * frame[:, :, 0]
    
    binarized = (greenery > 30) * 1.0

    x_sum = int(np.sum(x * binarized))
    y_sum = int(np.sum(y * binarized))
    n_sum = int(np.sum(binarized))

    if n_sum < 20:
        pos = prev_pos
    else:
        pos = (x_sum // n_sum, y_sum // n_sum)
        prev_pos = pos

    # cv2.imshow('frame', frame / 256 + np.stack([binarized, binarized, binarized], 2))
    cv2.imshow('frame', binarized)
    if (n_sum < 20):
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
    # print("Kamera")
    return pos


class CameraSensor(Device):
	
	def __init__(self, cam):
		init(cam)

	def get_data(self):
		return get_position()

class Heater(Device):

    def __init__(self, port, sleep: float = 0.04):
        Device.__init__(self, channel=2, port=port, sleep=sleep)
        self.bind_output_device(OutputSource.DAC)

    def send_data(self, temperature: int):
        self.actuate(temperature, 2)

class Tube(Device):

	def __init__(self, port, sleep=0.04, verbosity=False):
		self.sleep = sleep
		self.position_x = mp.Value('d', 0.0)
		self.position_y = mp.Value('d', 0.0)
		self.camera_process = mp.Process(target=self.camera_loop)
		Device.__init__(self, channel=5, port=port, verbosity=verbosity)
		self.fan = Heater(
			port=self.port,
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
		self.fan.send_data(command)


class BallAndTube(ApiBase):
	def __init__(self, port, verbosity= False):
		ApiBase.__init__(self)
		self.tube = Tube(port=port, verbosity=verbosity)

	def write_actuator(self, command):
		self.tube.send_data(command)

	def read_sensor_data(self):
		return self.tube.get_data()

	def exit(self):
		print("ocu da ga ubijem")
		self.tube.camera_process.terminate()