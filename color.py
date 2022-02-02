import machine

from TCS34725 import TCS34725

colors75 = [
    (69, 145, 198, 'schwarz'),
    (66, 143, 200, 'schwarz'),
    (75, 143, 197, 'schwarz'),
    (73, 142, 199, 'schwarz'),
    (72, 140, 200, 'braun'),
    (81, 142, 195, 'braun'),
    (90, 146, 188, 'braun'),
    (85, 143, 193, 'braun'),
    (51, 134, 211, 'blau'),
    (52, 134, 210, 'blau'),
    (50, 132, 212, 'blau'),
    (50, 132, 212, 'blau'),
    (93, 135, 194, 'violett'),
    (89, 134, 197, 'violett'),
    (89, 135, 196, 'violett'),
    (92, 133, 196, 'violett'),
    (125, 129, 180, 'rot'),
    (128, 128, 179, 'rot'),
    (127, 127, 179, 'rot'),
    (177, 112, 145, 'rot'),
    (134, 136, 168, 'orange'),
    (145, 133, 161, 'orange'),
    (151, 131, 157, 'orange'),
    (158, 129, 152, 'orange'),
    (136, 164, 139, 'gelb'),
    (140, 164, 135, 'gelb'),
    (131, 164, 144, 'gelb'),
    (139, 166, 134, 'gelb'),
    (62, 163, 186, 'gruen'),
    (65, 170, 178, 'gruen'),
    (63, 167, 182, 'gruen'),
    (62, 166, 183, 'gruen'),
    (134, 112, 185, 'pink'),
    (135, 111, 185, 'pink'),
    (145, 108, 179, 'pink'),
    (129, 115, 187, 'pink'),
    (113, 160, 162, 'weiss'),
    (118, 159, 160, 'weiss'),
    (109, 161, 164, 'weiss'),
    (118, 161, 158, 'weiss'),
]


class Color:
    def __init__(self):
        bus = machine.I2C(sda=machine.Pin(27), scl=machine.Pin(26))  # adjust pin numbers as per hardware
        self.tcs = TCS34725(bus)
        self.tcs.setGain(4)
        self.tcs.setIntegration_time(155)

        print("Gain", self.tcs.getGain())

    def getColor(self):
        v = self.readColor()
        return v

    def getColorFromList(self, v, colorList):
        c = colorList[0]
        e = 9999999999999
        for i in colorList:
            e2 = pow(i[0] - v[0], 2)
            e2 += pow(i[1] - v[1], 2)
            e2 += pow(i[2] - v[2], 2)
            if e2 < e:
                e = e2
                c = i
        return c + tuple([e])

    def readColor(self):
        return self.tcs.color_raw()[0:3]

    def readColorHsv(self):
        c = self.tcs.color_rgb_bytes()
        return self.rbg2hsv(c)

    def rbg2hsv(self, rbg):
        c = tuple((x / 255) for x in rbg[0:3])
        cmax = max(c)
        cmin = min(c)
        d = cmax - cmin
        r = c[0]
        g = c[1]
        b = c[2]

        if cmax == r:
            h = (((g - b) / d) % 6)
        elif cmax == g:
            h = ((b - r) / d) + 2
        else:  # blau
            h = ((r - g) / d) + 4

        h *= 60
        if h < 0:
            h += 360

        if cmax == 0:
            s = 0
        else:
            s = d / cmax

        print("RBG:", rbg, " H:", h, "S:", s, "V:", cmax)
        return tuple([h, s, cmax])
