from datetime import date, timedelta

d1 = date(2018, 8, 15,)  # start date
d2 = date(2018, 9, 23)  # end date

delta = d2-d1    # timedelta

#8547423544527376
daylst = []
for i in range(delta.days + 1):
    a = d1 + timedelta(days=i)
    print(a.strftime("%Y%m%d"))
    daylst.append(a)
