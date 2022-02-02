import machine

steps = [22, 37, 53, 70, 85, 99, 115, 130, 143, 158]

colorBinMap = {
    "schwarz": 0,
    "braun": 1,
    "weiss": 2,
    "pink": 3,
    "violett": 4,
    "blau": 5,
    "gruen": 6,
    "gelb": 7,
    "orange": 8,
    "rot": 9
}


class Servo:
    def __init__(self):
        self.servo = machine.PWM(machine.Pin(23), freq=50)
        self.setAngle(90)

    def setAngle(self, angle):
        # 0° = 30
        # 180° = 126
        self.servo.duty(int(((126 - 30) / 180 * angle) + 30))

    def setBin(self, index):
        if index == -1:
            self.setAngle(0)
            return
        self.setAngle(steps[index])

    def setBinByColor(self, color):
        try:
            self.setBin(colorBinMap[color])
        except KeyError:
            print("Unbekannte Farbe!!!: " + color)
            self.setAngle(0)

    def getBinNrByColor(self, color):
        try:
            return colorBinMap[color]
        except KeyError:
            print("Unbekannte Farbe!!!: " + color)
            return -1

    def getColorByBinNr(self, binNr):
        return list(colorBinMap.keys())[list(colorBinMap.values()).index(binNr)]
