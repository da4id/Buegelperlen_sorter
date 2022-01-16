import machine


class Servo:
    def __init__(self):
        self.servo = machine.PWM(machine.Pin(23), freq=50)
        self.setAngle(90)

    def setAngle(self, angle):
        # 0° = 30
        # 180° = 126
        self.servo.duty(int(((126 - 30) / 180 * angle) + 30))
