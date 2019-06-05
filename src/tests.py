oddMonths = ("01", "03", "05", "07", "09", "11")
evenMonths = ("04", "06", "08", "10", "12")
days = (
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"
    , "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "00", "00")

combo = "05"

def findmonth(entry, leap):
    if entry in oddMonths:
        return days[1:-2]
    if entry in evenMonths:
        return days[1:-3]
    if leap is True and int(entry) is 2:
        return days[1:-4]
    if leap is False and int(entry) is 2:
        return days[1:-5]


print(findmonth(combo, True))

