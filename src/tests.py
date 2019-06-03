import re

fin = open("stations_DB.csv", "r")
out = open("aaaa.csv", "w+")
for line in fin:
    withcomma = line.replace('|', ',')
    withoutspace = withcomma.replace(" ", "")
    output = re.sub(r"(?<![A-Z])(?<!^)([A-Z])",r" \1",withoutspace)
    out.write(output)