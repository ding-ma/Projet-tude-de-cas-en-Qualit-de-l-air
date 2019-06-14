import calendar
from datetime import date, timedelta


def aa():
    sMonth = 2
    eMonth = 3
    startDate = date(2019,sMonth,5)
    endDate = date(2019,eMonth,15)
    lstsMonth = []
    lsteMonth = []
    lstDays = []
    if sMonth is not eMonth:
        a= calendar.monthrange(2019,sMonth)[1]
        endMonth = date(2019,sMonth,a)
        delta1 = endMonth-startDate
        for f in range(delta1.days+1):
            a = startDate+timedelta(days=f)
            t = a.strftime("%d")
            lstsMonth.append(t)

        startMonth = date(2019,eMonth,1)
        delta2 = endDate-startMonth
        for q in range(delta2.days+1):
            c = startMonth+timedelta(days=q)
            w = c.strftime("%d")
            lsteMonth.append(w)
        return lstsMonth,lsteMonth
    else:
        delta = endDate-startDate
        for a in range(delta.days+1):
            e = startDate+timedelta(days=a)
            v = e.strftime("%d")
            lstDays.append(v)
        return lstDays


b = aa()
if len(b) is 2:
    a= ""
    for l in b[1]:
        a += l
    for z in b[0]:
        a +=z
    print(a)
else:
    print(b)

