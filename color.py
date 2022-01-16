import machine

from TCS34725 import TCS34725

colors75 = [
    (69, 145, 198, 'Schwarz'),
    (66, 143, 200, 'Schwarz'),
    (75, 143, 197, 'Schwarz stehend'),
    (73, 142, 199, 'Schwarz stehend'),
    (72, 140, 200, 'Braun'),
    (81, 142, 195, 'Braun'),
    (90, 146, 188, 'Braun stehend'),
    (85, 143, 193, 'Braun stehend'),
    (51, 134, 211, 'Blau'),
    (52, 134, 210, 'Blau'),
    (50, 132, 212, 'Blau stehend'),
    (50, 132, 212, 'Blau stehend'),
    (93, 135, 194, 'Violett'),
    (89, 134, 197, 'Violett'),
    (89, 135, 196, 'Violett stehend'),
    (92, 133, 196, 'Violett stehend'),
    (125, 129, 180, 'Rot'),
    (128, 128, 179, 'Rot'),
    (127, 127, 179, 'Rot stehend'),
    (177, 112, 145, 'Rot stehend'),
    (134, 136, 168, 'Orange'),
    (145, 133, 161, 'Orange'),
    (151, 131, 157, 'Orange stehend'),
    (158, 129, 152, 'Orange stehend'),
    (136, 164, 139, 'Gelb'),
    (140, 164, 135, 'Gelb'),
    (131, 164, 144, 'Gelb stehend'),
    (139, 166, 134, 'Gelb stehend'),
    # (74, 137, 201, 'Violett'),
    # (79, 135, 200, 'Violett'),
    # (86, 137, 197, 'Violett stehend'),
    # (79, 137, 200, 'Violett stehend'),
    # (94, 137, 193, 'Rot'),
    # (114, 132, 185, 'Rot'),
    # (116, 136, 181, 'Rot stehend'),
    # (116, 135, 181, 'Rot stehend'),
    # (131, 136, 171, 'Orange'),
    # (123, 137, 175, 'Orange'),
    # (102, 141, 186, 'Orange stehend'),
    # (116, 140, 179, 'Orange stehend'),
    # (108, 162, 164, 'Gelb'),
    # (123, 165, 151, 'Gelb'),
    # (111, 164, 160, 'Gelb stehend'),
    # (108, 162, 164, 'Gelb stehend'),

    (62, 163, 186, 'Gruen'),
    (65, 170, 178, 'Gruen'),
    (63, 167, 182, 'Gruen stehend'),
    (62, 166, 183, 'Gruen stehend'),
    (134, 112, 185, 'Pink'),
    (135, 111, 185, 'Pink'),
    (145, 108, 179, 'Pink stehend'),
    (129, 115, 187, 'Pink stehend'),
    (113, 160, 162, 'Weiss'),
    (118, 159, 160, 'Weiss'),
    (109, 161, 164, 'Weiss stehend'),
    (118, 161, 158, 'Weiss stehend'),

    # (98, 159, 172, 'Weiss'),
    # (106, 159, 167, 'Weiss'),
    # (109, 160, 165, 'Weiss stehend'),
    # (101, 160, 170, 'Weiss stehend'),

]


class Color:
    def __init__(self):
        bus = machine.I2C(sda=machine.Pin(27), scl=machine.Pin(26))  # adjust pin numbers as per hardware
        self.tcs = TCS34725(bus)
        self.tcs.setGain(4)

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
        return self.tcs.color_rgb_bytes()

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
