import color
import servo
import stepper

colorObj = color.Color()
servoObj = servo.Servo()

stepSize = 3
stepTime = 5


# 50 Schritte = 90° bei 1.8° pro Schritt

def initialise():
    print("Suche nächste Farbe....")
    stepper.moveToNextStop(stepSize, stepTime)


def getColorSmallSteps():
    # Drehen bis nicht mehr Rad als Farbe
    stepper.moveToNextStop(stepSize, stepTime)

    # Drehen bis Rad als Farbe und häufigste Farbe auswertern
    rawList = []
    while stepper.pos.value() == 0:
        if len(rawList) <= 5:
            rawList.append((0, 0, 0))
        else:
            rawList.append(colorObj.readColor())
        stepper.doSteps(stepSize, stepTime, 4)
    print("Anzahl Messungen: ", len(rawList))

    if 8 <= len(rawList) <= 13:
        rawColor = rawList[int(len(rawList) / 4 * 3)]
        c = colorObj.getColorFromList(rawColor, color.colors75)
        print("75%: ", c, " - Raw: ", rawColor)
        return c
    return False


def getNextColor():
    while getColorSmallSteps() == False:
        stepper.turnBack(stepSize, stepTime)
    stepper.doSteps(stepSize, stepTime, 350)
    stepper.moveToNextStop(stepSize, stepTime)


def doSorting():
    run = True
    tot = 0
    error = 0
    while run:
        tot = tot + 1
        getNextColor()
        r = input('korrekt?')
        if r == "q":
            run = False
        elif r == "y" or r == "":
            servoObj.setAngle(90)
        else:
            error = error + 1
            servoObj.setAngle(0)
    print('tot', tot, 'error', error)
