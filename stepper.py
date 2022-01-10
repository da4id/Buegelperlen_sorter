import time

from machine import Pin

step = Pin(32, Pin.OUT)
dir = Pin(33, Pin.OUT)

halfStep = Pin(17, Pin.OUT)
quarterStep = Pin(16, Pin.OUT)

dir.value(1)

pos = Pin(21, Pin.IN)


def doStep(divider, delay):
    halfStep.value(divider & 1)
    quarterStep.value((divider >> 1) & 1)

    step.value(0)
    time.sleep_ms(int(delay / 2))
    step.value(1)
    time.sleep_ms(int(delay / 2))


def doSteps(divider, delay, count):
    for i in range(0, count):
        doStep(divider, delay)

def moveToNextStop(stepSize, stepTime):
    while pos.value() == 1:
        doStep(stepSize, stepTime)