import color
import stepper

colorObj = color.Color()

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
    colorList = []
    rawList = []
    c = colorObj.getColor()
    while stepper.pos.value() == 0:
        rawList.append(colorObj.readColor())
        colorList.append(c)
        c = colorObj.getColor()
        stepper.doSteps(stepSize, stepTime, 4)
    print("Anzahl Messungen: ", len(colorList))
    colorStat = calcColorStatFromList(colorList)
    print("haufigste Farbe: ", colorStat)

    colorSmallestError = getColorWithSmallestErrorFromList(colorList)
    print("Farbe mit kleinstem Fehler: ", colorSmallestError)

    if 8 <= len(colorList) <= 13:
        print("25%", rawList[int(len(rawList) / 4)])
        print("50%", colorObj.getColorFromList(rawList[int(len(rawList) / 2)], color.colors50))
        print("75%", colorObj.getColorFromList(rawList[int(len(rawList) / 4 * 3)], color.colors75))

    return colorStat


def calcColorStatFromList(colorList):
    colorStat = {}
    for i in colorList:
        if i[2] in colorStat:
            colorStat[i[2]] += 1
        else:
            colorStat[i[2]] = 1
    return colorStat


def getColorWithSmallestErrorFromList(colorList):
    e = 999999
    c = color.colorsHs[0]
    for i in colorList:
        if i[3] < e:
            c = i
            e = i[3]
    return c


def getNextColor():
    c = getColorSmallSteps()
    print(c)
    stepper.doSteps(stepSize, stepTime, 350)
    stepper.moveToNextStop(stepSize, stepTime)
