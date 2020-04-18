import matplotlib.pyplot as plt
import pandas as pd 

from config import token

import pyEX as p
import os


ticker = 'AMD'
timeframe = '6m'

if os.path.exists("input.csv"):
    df = pd.read_csv("input.csv")
    print("Loaded from CSV")
else:
    c = p.Client(api_token=token)
    df = c.chartDF(ticker, timeframe)
    df.to_csv("input.csv")



df = df[['close']]
df.reset_index(level=0, inplace=True)
df.columns = ['ds', 'y']

exp1 = df.y.ewm(span=12, adjust=False).mean()
exp2 = df.y.ewm(span=26, adjust=False).mean()

macd = exp1-exp2


exp3 = macd.ewm(span=9, adjust=False).mean()

plt.plot(df.ds, macd, label='AMD MACD', color='#EBD2BE')
plt.plot(df.ds, exp3, label='Signal Line', color='#E5A4CB')

plt.legend(loc='upper left')

plt.show()

mcd = macd.to_frame()
expTest = exp3.to_frame()

mcd['y'] = mcd['y'].map('{:,.2f}'.format)
expTest['y'] = expTest['y'].map('{:,.2f}'.format)

# print(mcd)
# print(expTest)
compareResult = mcd[expTest.y.isin(mcd.y)]

list1 = compareResult['y'].tolist()
a = 0

starts = []
ends = []
starts.append(a)

while a < len(list1):
    # print(f"{a}/{len(list1)}")
    if a != 0:
        if list1[a - 1] < list1[a]:
            a += 1
        else:
            ends.append(a - 1)
            starts.append(a)
            a += 1
    else:
        a += 1
ends.append(a)

# print(starts, len(starts))
# print(ends, len(ends))

pairs = []
dealCounter = 0
while dealCounter < len(starts):
    pairs.append([starts[dealCounter], ends[dealCounter]])
    dealCounter += 1

# for a in pairs:
#     print(a)

df = pd.read_csv("test.csv")

totalDeals = []
dealDate = df.date.tolist()
dealOpen = df.open.tolist()
dealClose = df.close.tolist()

for pair in pairs:
    totalDeals.append([dealDate[pair[0]], dealDate[pair[1]], dealOpen[pair[0]], dealClose[pair[1]]])

newDF = pd.DataFrame(totalDeals, columns=['start', 'end', 'open', 'close'])
# print(newDF)

df.to_csv("output.csv")











