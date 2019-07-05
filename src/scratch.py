import datetime

start = datetime.datetime(2019, 5, 30)
end = datetime.datetime(2019, 6, 2)
delta = end - start

lstYMD=[]
for i in range(delta.days + 1):
    date = start + datetime.timedelta(days=i)
    lstYMD.append(date.strftime("%Y/%m/%d"))
print(lstYMD)

for l in lstYMD:
    print(l.split("/"))
# templst = []
# path = os.getcwd()
# for files in os.listdir(path+"/output"):
#     if files.startswith("GEM__ID100103___00O3___Start20190530___End20190602"):
#         templst.append(files)
#
# sortedtemplst = sorted(templst)
# firstFile = open(path+"/output/"+sortedtemplst[0], "r")
# secondFile = open(path+"/output/"+sortedtemplst[1], "r")
#
# firstreader = csv.reader(firstFile)
# firstList = list(firstreader)
#
# secondreader = csv.reader(secondFile)
# secondList = list(secondreader)
#
# number =0
# for days,number in zip(lstYMD,range(len(lstYMD))):
#     print(number)
#     endIndex = number+1
#     write1 = firstList[number*24:endIndex*24]
#     write2 = secondList[number*24:endIndex*24]
#     csvfile = open(path+"/output/GEM__ID100103___00O3___"+str(days)+".csv","w+", newline="")
#     csvfile.write("Date,Time,Height,Value\n")
#     wr = csv.writer(csvfile,quoting=csv.QUOTE_ALL)
#     for l1 in write1:
#         wr.writerow(l1)
#     for l2 in write2:
#         wr.writerow(l2)
#     print("==========")