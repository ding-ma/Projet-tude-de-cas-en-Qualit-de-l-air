import os
import shutil


def movefile():
    source = "M:\Projet-tude-de-cas-en-Qualit-de-l-air\src\out"
    particules = ["N2", "O3"]
    modelh = ["00", "O3"]

    for p in particules:
        for m in modelh:
            destination = "M:\Projet-tude-de-cas-en-Qualit-de-l-air\src\out"+m+p
            if not os.path.exists(destination+m+p):
                os.makedirs(destination+m+p)
            for f in os.listdir(source):
                if f.endswith(m+p+".csv"):
                    shutil.move(source + f, destination+m+p)


#movefile()
deletelist = os.listdir("M:\Projet-tude-de-cas-en-Qualit-de-l-air\src\out\\")

for d in deletelist:
    shutil.rmtree("/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out/"+d)

particules = ["N2", "O3"]
modelh = ["00", "12"]

destination = "/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/out/"
for m in modelh:
    for p in particules:
        if not os.path.exists(destination + m + p):
            os.makedirs(destination + m + p)
        for f in os.listdir(destination):
            if f.endswith("_"+m + p + ".csv"):
                shutil.move(destination + f, destination + m + p)
        file = open("output"+m+p+".csv", "w+")
        for i in os.listdir(destination+m+p):
            b = open(destination+m+p+"/"+i).read()
            file.write(b)