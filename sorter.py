import color
import colorMap
import servo
import stepper

colorObj = color.Color()
servoObj = servo.Servo()

stepSize = 3
stepTime = 5

errorLimit = 1500
trainingActive = False
trainingAll = False


# 50 Schritte = 90° bei 1.8° pro Schritt

def initialise():
    print("Suche nächste Farbe....")
    stepper.moveToNextStop(stepSize, stepTime, 600)


def getColorSmallSteps():
    # Drehen bis nicht mehr Rad als Farbe
    stepper.moveToNextStop(stepSize, stepTime, 450)

    # Drehen bis Rad als Farbe und häufigste Farbe auswertern
    rawList = []
    while stepper.pos.value() == 0:
        if len(rawList) <= 5 or len(rawList) >= 10:
            rawList.append((0, 0, 0))
        else:
            rawList.append(colorObj.readColor())
        stepper.doSteps(stepSize, stepTime, 4)
    print("Anzahl Messungen: ", len(rawList))

    if 8 <= len(rawList) <= 13:
        rawColor = rawList[int(len(rawList) / 4 * 3)]
        c = colorObj.getColorFromList(rawColor, colorMap.learningColorMap)
        print("75%: ", c, " - Raw: ", rawColor, servoObj.getColorByBinNr(c[3]))

        if trainingActive:
            if trainingAll or c[4] > errorLimit:
                colorStr = input("korrekte Farbe (enter für ok): ")
                if c[4] > errorLimit or colorStr != "":
                    if colorStr == "":
                        binNr = c[3]
                        colorStr = servoObj.getColorByBinNr(binNr)
                    else:
                        binNr = servoObj.getBinNrByColor(colorStr)
                    print("Speichere Farbe ", colorStr, binNr)
                    colorMap.learningColorMap.append(
                        (rawColor[0], rawColor[1], rawColor[2], binNr))
                    c = colorObj.getColorFromList(rawColor, colorMap.learningColorMap)
        return c
    return False


def getNextColor():
    c = getColorSmallSteps()
    while c == False:
        stepper.turnBack(stepSize, stepTime)
        c = getColorSmallSteps()
    servoObj.setBin(c[3])
    stepper.doSteps(stepSize, stepTime, 350)
    stepper.moveToNextStop(stepSize, stepTime, 450)


def doSorting():
    run = True
    tot = 0
    while run:
        tot = tot + 1
        getNextColor()
    print('tot', tot)
