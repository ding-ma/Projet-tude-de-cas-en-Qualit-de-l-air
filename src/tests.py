import os

filelocation = os.getcwd()

directories = ["bash", "config", "rarc", "output", "extracted"]

for i in directories:
    if not os.path.exists(filelocation+"/"+i):
        os.mkdir(filelocation+"/"+i)

filedirectory = next(os.walk('.'))[1]
print(filelocation)