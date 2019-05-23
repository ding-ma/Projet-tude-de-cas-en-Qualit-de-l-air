import os
import time
days = (
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"
    , "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")

hours = (
    "000", "001", "002", "003", "004", "005", "006", "007", "008", "009", "010", "011", "012", "013", "014", "015",
    "016",
    "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", "030", "031", "032",
    "033",
    "034", "035", "036", "037", "038", "039", "040", "041", "042", "043", "044", "045", "046", "047", "048")

path = '/space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/bashtest/operation.forecasts.mach/operation.forecasts.mach/'
sHourIndex = 0
eHoursIndex = 4
lstdays = list(days[0:2])
lsthours = list(hours[sHourIndex:eHoursIndex + 1])

newlst = []
lst1 = []
i = 0
for d in lstdays:
    for h in lsthours:
        a = os.path.isfile(path + '201905' + d + '12_' + h)
        newlst.append(a)
        lst1.append(d + " " + h)
        abc = open("gem/gemmach" + d + "_" + h + ".txt", 'w+')
        abc.write('ping 172.217.13.16' + str(i))
        i = i + 1
print(newlst)
print(lst1)

i = 0
lst = []
for t in newlst:
    if t is False:
        lst.append(lst1[i])
    i = i + 1
beg = lst[0]
end = lst[-1]
aaa = beg.split(" ")
bbb = end.split(" ")
print(lst)
print("m: " + aaa[0], "d: " + aaa[1], "      end ", "m: " + bbb[0], "d: " + bbb[1])

print(os.listdir('gem'))

for a in os.listdir('gem'):
    abc = open("gem/" + a, 'r').read()
    os.system(abc)
print(time.clock())
# a=os.system("rarc -i /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/gemmach &")
# b=os.system("rarc -i /space/hall1/sitestore/eccc/oth/airq_central/sair001/Ding_Ma/gemmach1 &")
