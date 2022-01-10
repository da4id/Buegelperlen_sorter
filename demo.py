import machine
from tcs3472 import tcs3472
from machine import Pin
import neopixel
import math

bus = machine.I2C(sda=machine.Pin(27), scl=machine.Pin(26)) # adjust pin numbers as per hardware
tcs = tcs3472(bus)


pixels = neopixel.NeoPixel(Pin(21, Pin.OUT), 1)
while True:
    a = tcs.rgb()
    pixels[0] = (a[0]>>2,a[1]>>2,a[2]>>2)
    pixels.write()

while True:
    a = tcs.raw()
    pixels[0] = (a[1],a[2],a[3])
    pixels.write()

v = tcs.rgb()+ tuple([tcs.brightness()])

rad = (27,84, 128,145,'rad')
orangeL  (74, 81, 90, 151,'orange')
orange = (70, 82, 91, 153, 'orange')
orange = (63, 75, 101, 88, 'orange')
orange = (64, 76, 101, 85, 'orange')
orange = (70, 76, 95, 92, 'orange')
braunS =(50, 83, 107, 59, 'braun')
braunL= (48, 84, 107, 89, 'braun')
braun = (42, 81, 114, 58, 'braun')
braun = (41, 82, 115, 70, 'braun')
schwarzL=(37, 82, 116, 58,'schwarz')
schwarzL=(29, 83, 125, 63, 'schwarz')
schwarz=(35, 83, 118, 58, 'schwarz')
schwarz=(34, 83, 120, 63, 'schwarz')
gruen = (40, 89, 106, 72, 'gruen')
gelb = (64, 85, 87, 93, 'gelb')
gelb = (59, 84, 98, 138, 'gelb')
weiss = (53, 86, 104, 143, 'weiss')
weiss = (59, 84, 99, 176, 'weiss')
blau = (57, 83, 103, 143, 'blau')
rot = (63, 74, 105, 79, 'rot')
pink = (73, 72, 95, 150, 'pink')
braun = (42, 81, 114, 58, 'braun')
braun = (41, 82, 115, 70, 'braun')


colors = [
(27,84, 128,145,'rad'),
(74, 81, 90, 151,'orange'),
(70, 82, 91, 153, 'orange'),
(63, 75, 101, 88, 'orange'),
(64, 76, 101, 85, 'orange'),
(70, 76, 95, 92, 'orange'),
(50, 83, 107, 59, 'braun'),
(48, 84, 107, 89, 'braun'),
(42, 81, 114, 58, 'braun'),
(41, 82, 115, 70, 'braun'),
(37, 82, 116, 58,'schwarz'),
(29, 83, 125, 63, 'schwarz'),
(35, 83, 118, 58, 'schwarz'),
(34, 83, 120, 63, 'schwarz'),
(40, 89, 106, 72, 'gruen'),
(64, 85, 87, 93, 'gelb'),
(59, 84, 98, 138, 'gelb'),
(53, 86, 104, 143, 'weiss'),
(59, 84, 99, 176, 'weiss'),
(57, 83, 103, 143, 'blau'),
(63, 74, 105, 79, 'rot'),
(73, 72, 95, 150, 'pink'),
(42, 81, 114, 58, 'braun'),
(41, 82, 115, 70, 'braun')
]

v = tcs.rgb()+ tuple([tcs.brightness()])
c = colors[0]
e = 9999999999999
for i in colors:
    e2 = pow(i[0]-v[0],2)
    e2 += pow(i[1]-v[1],2)
    e2 += pow(i[2]-v[2],2)
    e2 += pow(i[3]-v[3],2)
    if e1 < e:
        print("neue Farbe gefunden", i)
        e = e1
        c = i
print(c)
