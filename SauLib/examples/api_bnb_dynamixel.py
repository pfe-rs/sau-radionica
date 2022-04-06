from api_base import ApiBase
import multiprocessing as mp
import bnb_dynamixel as bnb_dynamixel


class ApiBnbDynamixel(ApiBase):

    def __init__(self, camera_port=0, motor_port='/dev/ttyUSB0'):
        ApiBase.__init__(self)
        self.camera_process = mp.Process(target=self.camera_loop)
        self.pos_mutex = mp.Lock()
        self.position = mp.Value('d', 0.0)
        self.photo_id = mp.Value('i', 0)
        bnb_dynamixel.init(arg_port_name=motor_port,
                           arg_camera_select=camera_port)
        self.camera_process.start()

    def camera_loop(self):
        while True:
            tmp_pos = bnb_dynamixel.get_position()
            self.position.value = tmp_pos[0] if tmp_pos is not None else 0

    def read_sensor_data(self):
        tmp_pos = self.position.value
        return tmp_pos

    def control(self, measurement):
        return None

    def write_actuator(self, command):
        bnb_dynamixel.set_angle(command)
