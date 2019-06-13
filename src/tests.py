from datetime import date, timedelta

d1 = date(2018, 8, 15,)  # start date
d2 = date(2018, 9, 5)  # end date

delta = d2-d1    # timedelta

#8547423544527376
yearlst =[]
monthlst = []
daylst = []
fulllst = []
for i in range(delta.days + 1):
    a = d1 + timedelta(days=i)
    year = a.strftime("%Y")
    date = a.strftime("%d")
    month = a.strftime("%m")
    full = a.strftime("%Y%m%d")
    fulllst.append(full)
    yearlst.append(year)
    monthlst.append(month)
    daylst.append(date)

a = set(monthlst)
for b in a:
    print(b)
for y,m,d in zip(yearlst,monthlst,daylst):
    print(y+m+d)
