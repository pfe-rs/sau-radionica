# Libraries

import serial
import cv2
import numpy as np

# Setup variables

port_name = '/dev/ttyUSB0'
camera_select = 0

# Helper functions and variables

ser = None
cap = None
width, height = None, None
x, y = None, None
mid_angle = 512
min_angle = mid_angle - 100
max_angle = mid_angle + 100


def set_dyn_angle(pos):
    global ser

    if pos < min_angle: pos = min_angle
    if pos > max_angle: pos = max_angle
    pos_l = pos & 0xff
    pos_h = pos >> 8
    header = [255, 255]
    msg = [1, 5, 3, 30, pos_l, pos_h]
    chkSum = [(~sum(msg)) & 0xff]
    instruction_packet = header + msg + chkSum
    ser.write(bytes(instruction_packet))


def set_dyn_speed(spd):
    global ser

    spd_l = spd & 0xff
    spd_h = spd >> 8
    header = [255, 255]
    msg = [1, 5, 3, 32, spd_l, spd_h]
    chkSum = [(~sum(msg)) & 0xff]
    instruction_packet = header + msg + chkSum
    ser.write(bytes(instruction_packet))


# Main code

def init(arg_port_name='/def/ttyUSB0/', arg_camera_select=0):
    global cap, width, height, x, y, ser, port_name, camera_select

    port_name = arg_port_name
    camera_select = arg_camera_select

    cap = cv2.VideoCapture(camera_select)
    ret, frame = cap.read()

    height, width = frame[:, :, 0].shape
    x, y = np.meshgrid(np.linspace(0, width - 1, width),
                       np.linspace(0, height - 1, height))
    ser = serial.Serial(port_name, baudrate=1000000)

    set_dyn_speed(300)
    set_dyn_angle(512)


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
        pos = None
    else:
        pos = (x_sum // n_sum, y_sum // n_sum)
        x_pos, y_pos = pos

    # cv2.imshow('frame', frame / 256 + np.stack([binarized, binarized, binarized], 2))
    # cv2.imshow('frame', greenery / 256)
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
    return pos


def set_angle(ang):
    set_dyn_angle(int(ang))
