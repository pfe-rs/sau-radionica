import sys

sys.path.append("..\\..")

from hw.sau_api.api_heater_diy import DryerDiy

# Set port name
PORT = 'COM6'


class TestDryer(DryerDiy):

    integral = 0
    target = 373

    def control(self, measurement):
        print(measurement)
        self.integral -= measurement-self.target
        return (self.target-measurement)//4+128+self.integral//1000


tst = TestDryer(port=PORT, verbosity=False)
tst.control_loop()
