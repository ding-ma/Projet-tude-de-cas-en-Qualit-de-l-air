import csv

def search_cell(string):
    with open('aaaa.csv', 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            for j, column in enumerate(row):
                if string in column:
                    print((i,j))
                    return i
    print('nope')
    return 'nope'

print(search_cell("Pictou"))