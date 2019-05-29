import os
import re
import shutil

filelocation = os.getcwd()
formattedParticuleString = "O3 AF"
modelHour = "00"

def sortAndGenerate(destination):
    print(destination)
    particulelist = re.split(" ", formattedParticuleString)
    modelHourList = re.split(",", modelHour)
    for m in modelHourList:
        for p in particulelist:
            print(os.path.exists(destination + m + p))
            if not os.path.exists(destination + m + p):
                os.makedirs(destination + m + p)
            for f in os.listdir(destination):
                if f.endswith("_" + m + p + ".csv"):
                    shutil.move(destination + f, destination + m + p)
            file = open("output" + m + p + ".csv", "w+")
            for i in os.listdir(destination + m + p):
                b = open(destination + m + p + "/" + i).read()

                file.write(b)


sortAndGenerate(filelocation+"/extracted/")