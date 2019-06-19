import sys
file = open("Eticket.txt", "r")
eticket = file.read()
array = eticket.split(" ")
if len(array) is 2:
    for l in array:
        if l.startswith("CAPAMIST"):
            print("good")
        else:
            sys.exit(-9)

