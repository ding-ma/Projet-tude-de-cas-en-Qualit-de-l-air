from datetime import datetime, timedelta

for i in range(48+1):
    nine_hours_from_now = datetime(2011,12,31,12) + timedelta(hours=i)
    print(nine_hours_from_now.strftime("%H"))
