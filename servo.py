import machine

steps = [22, 37, 53, 70, 85, 99, 115, 130, 143, 158]


class Servo:
    def __init__(self):
        self.servo = machine.PWM(machine.Pin(23), freq=50)
        self.setAngle(90)

    def setAngle(self, angle):
        # 0° = 30
        # 180° = 126
        self.servo.duty(int(((126 - 30) / 180 * angle) + 30))

    def setBin(self, index):
        self.setAngle(steps[index])
