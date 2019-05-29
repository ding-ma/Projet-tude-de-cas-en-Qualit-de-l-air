import csv
import os


# with open("2018012000.txt", "r") as f:
#     result = '\n'.join(f.readlines())
#
# with open("output.csv", "w+") as f:
#     for line in result.split('\n'):
#         line = line.replace('|', ',')
#         f.write(line + '\n')

def toCSV():
    for a in os.listdir("csvconvert"):
        with open("csvconvert\\"+a, "r") as infile, open("csvconverted\\"+a+".csv",'w') as outfile:
            for line in infile:
                withcomma = line.replace('|',',')
                withoutspace = withcomma.replace(" ", "")
                outfile.write(withoutspace)



file = open("UMOS_Ref.csv", "r")
reader = csv.reader(file)
UMOSRefList = list(reader)
lstStationID = []
lstUMOSID = []

for x in range(len(UMOSRefList)):
    line = UMOSRefList[x]
    stationID = line[1]
    lstStationID.append(stationID)
    UMOSID = line[2]
    lstUMOSID.append(UMOSID)

referenceDict = dict(zip(lstUMOSID,lstStationID))

file = open("csvconverted\\2017010212_csv.csv", "r")
reader = csv.reader(file)
lsttoconvert = list(reader)
reflst = []
#list of letters
print(lsttoconvert)
# for y in range(len(lsttoconvert)):
#     line = lsttoconvert[y]
#     ref = line[2]
#     reflst.append(ref)
#
# f = open("out.csv", "w")
# #list of numbers
# lsta = []
#
# l=3
# for row in lsttoconvert[3:]:
#     a = row[2]
#     b = referenceDict[a]
#     lsttoconvert[l][2] = b
#     l=l+1
#
# print(lsttoconvert)
# # for q in lsttoconvert:
# #     print(q)
