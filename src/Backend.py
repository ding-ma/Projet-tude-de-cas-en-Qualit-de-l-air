# checks for date input errors
def inputDate(date):
    unformatattedDate = date.split("/")
    year = unformatattedDate[0]
    month = unformatattedDate[1]
    day = unformatattedDate[2]

    oddMonths = ("01", "03", "05", "07", "09", "11")
    evenMonths = ("04", "06", "08", "10", "12")

    if len(year) != 4 or len(month) != 2 or month > "12" or len(day) != 2:
        dateErrors()
    elif month == "02" and int(day) > 28:
        dateErrors()
    elif month in oddMonths and int(day) > 31:
        dateErrors()
    elif month in evenMonths and int(day) > 30:
        dateErrors()
    else:
        print(year, month, day)

def dateErrors():
    print("Date format error enter them again")

