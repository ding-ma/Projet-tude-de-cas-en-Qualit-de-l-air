days = (
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18",
    "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
sDay = "10"
eDay = "15"

sIndex = days.index(sDay)
eIndex = days.index(eDay)
unformattedDay = ""
for dayList in range(eIndex - sIndex + 1):
    unformattedDay += days[sIndex + dayList]
formattedDay = ' '.join(unformattedDay[i:i + 2] for i in range(0, len(unformattedDay), 2))
print(formattedDay)
