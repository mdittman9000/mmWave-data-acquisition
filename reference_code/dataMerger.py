
from pathlib import Path

path = "data/"

imag_files = [path for path in Path('data').rglob('*.imsession')]
path = "data\\Bottom-to-top_swipe\\Bottom-to-top_swipe_07_02_2021_14_22_45"


for i in range(len(imag_files)):

    path = "\\".join(str(imag_files[i]).split('\\')[:-1])

    dataRaw = open(path + "\\adcExtractedData.csv","r")
    dataPoint = open(path + "\\sampledData.csv", "r")
    dataMerged = open(path + "\\fullData.csv","w")

    rawHeader = str(dataRaw.readline())
    pointHeader = str(dataPoint.readline())


    fullHeader = rawHeader.strip() + ',' + ','.join(pointHeader.split(",")[1:])

    dataMerged.write(fullHeader)

    keepReading = True
    rawEmpty = False
    pointEmpty = False

    rawIdx = 0
    pointIdx = 0
    lineIdx = 0

    linesRaw = dataRaw.readlines()
    linesPoint = dataPoint.readlines()
    linesFull = []

    while keepReading:

        lineIdx = lineIdx + 1
        
        if rawIdx == len(linesRaw) - 1:
            rawEmpty = True
            if pointEmpty:
                break
        if pointIdx == len(linesPoint) - 1:
            pointEmpty = True
            if rawEmpty:
                break

        if rawEmpty:
            while pointIdx < len(linesPoint):
                linesFull.append(str(linesPoint[pointIdx].split(",")[0]) + ',' + ','.join(linesRaw[rawIdx].strip().split(",")[1:]) + ',' + ','.join(linesPoint[pointIdx].split(",")[1:]))
                pointIdx = pointIdx + 1

            break

        if pointEmpty:
            while rawIdx < len(linesRaw):
                linesFull.append(linesRaw[rawIdx].strip() + ',' + ','.join(linesPoint[pointIdx].split(",")[1:]))
                rawIdx += rawIdx + 1

            break

        timeRaw = float(linesRaw[rawIdx].split(",")[0])
        timePoint = float(linesPoint[pointIdx].split(",")[0])


        if abs(timeRaw - timePoint) > 0.001:
            if timeRaw < timePoint:
                linesFull.append(linesRaw[rawIdx].strip() + ',' + ','.join(linesPoint[pointIdx].split(",")[1:]))
                rawIdx = rawIdx + 1
            elif timeRaw > timePoint:
                linesFull.append(str(linesPoint[pointIdx].split(",")[0]) + ',' + ','.join(linesRaw[rawIdx].strip().split(",")[1:]) + ',' + ','.join(linesPoint[pointIdx].split(",")[1:]))
                pointIdx = pointIdx + 1
        else:
            print(timeRaw, timePoint)
            print("equal point")
            rawIdx = rawIdx + 1
            pointIdx = pointIdx + 1



    dataMerged.writelines(linesFull)


    dataRaw.close()
    dataPoint.close()
    dataMerged.close()
