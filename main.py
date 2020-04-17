import matplotlib.pyplot as plt

# token расположен в файле config.py
from config import token

# библиотека для работы API https://iexcloud.io/
import pyEX as p


c = p.Client(api_token=token)

ticker = 'AMD'
timeframe = '6m'

df = c.chartDF(ticker, timeframe)
df = df[['close']]
df.reset_index(level=0, inplace=True)
df.columns = ['ds', 'y']

exp1 = df.y.ewm(span=12, adjust=False).mean()
exp2 = df.y.ewm(span=26, adjust=False).mean()

# рассчет MACD
macd = exp1-exp2

exp3 = macd.ewm(span=9, adjust=False).mean()

plt.plot(df.ds, macd, label='AMD MACD', color='#EBD2BE')
plt.legend(loc='upper left')

# вывод MACD на экран
plt.show()
