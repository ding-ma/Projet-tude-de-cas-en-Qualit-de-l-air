import os

# with open("2018012000.txt", "r") as f:
#     result = '\n'.join(f.readlines())
#
# with open("output.csv", "w+") as f:
#     for line in result.split('\n'):
#         line = line.replace('|', ',')
#         f.write(line + '\n')

for l in os.listdir("testingUMOsfile"):
    os.system("cat /fs/site1/dev/eccc/oth/airq_central/sair001/Ding_Ma/testingUMOsfile/"+l+ "| grep INU > /fs/site1/dev/eccc/oth/airq_central/sair001/Ding_Ma/testing/"+l)

def toCSV():
    for a in os.listdir("testingUMOsfile"):
        with open("testing/"+a, "r") as infile, open("converted/"+a+".csv",'w') as outfile:
            for line in infile:
                withcomma = line.replace('|',',')
                withoutspace = withcomma.replace(" ", "")
                outfile.write(withoutspace)

toCSV()