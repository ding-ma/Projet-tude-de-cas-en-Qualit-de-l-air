#https://stackoverflow.com/questions/42583664/pandas-merge-csv-base-on-columns

import pandas as pd
# df1 = pd.read_csv("rarc/00.csv")
# df2 = pd.read_csv("rarc/12.csv")
#
# print(df1)
# dfout = df1.merge(df2, how='inner', on=['Date','Time'])
# dfout.to_csv('rarc/out.csv',index=False)

# Create a Pandas dataframe from some data.
df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('rarc/00.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Apply a conditional format to the cell range.
worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})

# Close the Pandas Excel writer and output the Excel file.
writer.save()