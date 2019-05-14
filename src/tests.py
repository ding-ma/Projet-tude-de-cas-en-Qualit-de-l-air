hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016",
    "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
    "033",
    "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")

start = "000"
end = "013"

startIndex = hours.index(start)

endIndex = hours.index(end)


file = open("gemmach", "w")


for x in range(endIndex - startIndex + 1):
    file.write("," + hours[startIndex + x])


def aaa():
    modelHour = abc()
    print(modelHour)


def abc():
    h_00 = True
    h_12 = True
    if h_00 is True and h_12 is False:
        modelHour = "00"
        return modelHour
    elif h_12 is True and h_00 is False:
        modelHour = "12"
        return modelHour
    elif h_12 and h_00 is True:
        modelHour = "00,12"
        return modelHour


azq = 55
print(bool(azq))
