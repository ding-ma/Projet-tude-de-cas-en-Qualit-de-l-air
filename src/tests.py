listMonth = ("00","01","02","03","04","05","06","07","08","09","10","11","12")

sMonth = "01"
eMonth = "10"

sIndex = listMonth.index(sMonth)
eIndex = listMonth.index(eMonth)
unformattedMonthList =""
for monthList in range(eIndex-sIndex+1):
    unformattedMonthList += listMonth[sIndex+monthList]
    formattedMonthlist = ' '.join(unformattedMonthList[i:i + 2] for i in range(0, len(unformattedMonthList), 2))
print(formattedMonthlist)

abc = False
print(int(abc))