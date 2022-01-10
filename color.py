import machine

from TCS34725 import TCS34725

colors50 = [
    (56, 135, 208, 'Blau'),
    (54, 134, 209, 'Blau'),
    (122, 114, 191, 'Pink stehend'),
    (143, 113, 177, 'Pink stehend'),
    (133, 136, 170, 'Orange'),
    (124, 135, 176, 'Orange'),
    (89, 145, 190, 'Braun'),
    (78, 141, 197, 'Braun'),
    (103, 154, 174, 'Gelb stehend'),
    (112, 157, 167, 'Gelb stehend'),
    (58, 140, 205, 'Schwarz'),
    (64, 142, 201, 'Schwarz'),
    (69, 176, 170, 'Gruen'),
    (63, 165, 183, 'Gruen'),
    (80, 148, 192, 'Schwarz stehend'),
    (69, 143, 199, 'Schwarz stehend'),
    (121, 129, 183, 'Rot'),
    (117, 131, 184, 'Rot'),
    (73, 166, 179, 'Gruen stehend'),
    (63, 161, 187, 'Gruen stehend'),
    (111, 152, 170, 'Weiss'),
    (112, 153, 170, 'Weiss'),
    (76, 132, 204, 'Violett stehend'),
    (69, 133, 206, 'Violett stehend'),
    (119, 158, 159, 'Weiss stehend'),
    (90, 150, 185, 'Weiss stehend'),
    (161, 102, 169, 'Pink'),
    (159, 102, 171, 'Pink'),
    (84, 133, 200, 'Violett'),
    (96, 134, 194, 'Violett'),
    (114, 133, 185, 'Orange stehend'),
    (127, 132, 177, 'Orange stehend'),
    (62, 138, 205, 'Braun stehend'),
    (65, 139, 203, 'Braun stehend'),
    (139, 158, 142, 'Gelb'),
    (135, 159, 147, 'Gelb'),
    (97, 131, 195, 'Rot stehend'),
    (82, 133, 201, 'Rot stehend'),
    (51, 134, 211, 'Blau stehend'),
    (47, 131, 213, 'Blau stehend'),
]

colors75 = [
    (51, 134, 211, 'Blau'),
    (52, 134, 210, 'Blau'),
    (145, 108, 179, 'Pink stehend'),
    (129, 115, 187, 'Pink stehend'),
    (134, 136, 168, 'Orange'),
    (145, 133, 161, 'Orange'),
    (72, 140, 200, 'Braun'),
    (81, 142, 195, 'Braun'),
    (131, 164, 144, 'Gelb stehend'),
    (139, 166, 134, 'Gelb stehend'),
    (69, 145, 198, 'Schwarz'),
    (66, 143, 200, 'Schwarz'),
    (62, 163, 186, 'Gruen'),
    (65, 170, 178, 'Gruen'),
    (75, 143, 197, 'Schwarz stehend'),
    (73, 142, 199, 'Schwarz stehend'),
    (125, 129, 180, 'Rot'),
    (128, 128, 179, 'Rot'),
    (63, 167, 182, 'Gruen stehend'),
    (62, 166, 183, 'Gruen stehend'),
    (113, 160, 162, 'Weiss'),
    (118, 159, 160, 'Weiss'),
    (89, 135, 196, 'Violett stehend'),
    (92, 133, 196, 'Violett stehend'),
    (109, 161, 164, 'Weiss stehend'),
    (118, 161, 158, 'Weiss stehend'),
    (134, 112, 185, 'Pink'),
    (135, 111, 185, 'Pink'),
    (93, 135, 194, 'Violett'),
    (89, 134, 197, 'Violett'),
    (151, 131, 157, 'Orange stehend'),
    (158, 129, 152, 'Orange stehend'),
    (90, 146, 188, 'Braun stehend'),
    (85, 143, 193, 'Braun stehend'),
    (136, 164, 139, 'Gelb'),
    (140, 164, 135, 'Gelb'),
    (127, 127, 179, 'Rot stehend'),
    (177, 112, 145, 'Rot stehend'),
    (50, 132, 212, 'Blau stehend'),
    (50, 132, 212, 'Blau stehend'),
]

colors = [
    (140, 126, 171, 'rot'),
    (56, 136, 208, 'blau'),
    (63, 145, 200, 'schwarz'),
    (161, 102, 168, 'pink'),
    (152, 135, 153, 'orange'),
    (82, 147, 190, 'braun'),
    (145, 161, 134, 'gelb'),
    (87, 134, 198, 'violett'),
    (96, 174, 172, 'gruen'),
    (117, 156, 163, 'weiss'),
]

colorsHs = [
    (259, 0.263, 'rot'),
    (220, 0.75, 'blau'),
    (204, 0.685, 'schwarz'),
    (293, 0.39, 'pink'),
    (297, 0.11, 'orange'),
    (204, 0.57, 'braun'),
    (95, 0.167, 'gelb'),
    (214, 0.56, 'violett'),
    (179, 0.6, 'grun'),
    (189, 0.282, 'weiss'),
]


class Color:
    def __init__(self):
        bus = machine.I2C(sda=machine.Pin(27), scl=machine.Pin(26))  # adjust pin numbers as per hardware
        self.tcs = TCS34725(bus)
        self.tcs.setGain(4)

        print("Gain", self.tcs.getGain())

    def getColor(self):
        v = self.readColorHsv()
        return self.getColorHsvFromList(v, colorsHs)

    def getColorHsvFromList(self, v, colorList):
        c = colorsHs[0]
        e = 9999999999999
        for i in colorList:
            e2 = pow((i[0] - v[0]), 2)
            e2 += pow(i[1] - v[1], 2)
            if e2 < e:
                e = e2
                c = i
        return c + tuple([e])

    def getColorFromList(self, v, colorList):
        c = colors[0]
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
