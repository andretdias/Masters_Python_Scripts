import pandas as pd

data1 = pd.read_csv(input('Enter de 1st file name: '))
data1 = data1.iloc[: , :-1]
header = list(data1.columns)
header1 = []
for element in header:
    if 'Unnamed' in element:
        element = ''
        header1.append(element)
    else:
        header1.append(element)

data2 = pd.read_csv(input('Enter the 2nd file name: '))
header2 = list(data2.columns)
for element in header2:
    if 'Unnamed' in element:
        element = ''
        header1.append(element)
    else:
        header1.append(element)

data = pd.concat([data1, data2], axis = 1)
data.columns = header1
data.to_csv('combined.csv', index = False)
