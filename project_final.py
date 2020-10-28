import json
from pprint import pprint
import datetime
from dateutil.relativedelta import relativedelta
import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms



url = "https://efts.sec.gov/LATEST/search-index"
form = {"q":"\"pdufa\" \"goal date\" ","dateRange":"custom","startdt":"2020-09-01","enddt":"2020-10-26","category":"all","locationType":"located","locationCode":"all","filter_forms":"8-K","page":"1","from":0}
form_data = json.dumps(form)

result = requests.post(url, data=form_data).text

first_data = []

second_data = []

final_data = []

second_data = final_data

for d in json.loads(result)['hits']['hits']:
    comp_profile = d["_source"]
    first_data.append(comp_profile)

seen = []
cleaned = []
for data in first_data:
    if data['display_names'] not in seen:
        cleaned.append(data)
        seen.append(data['display_names'])


for i in cleaned:
    company = i["display_names"]
    date = i['file_date']

    clean_data = {}
    clean_data["Company name and ticker: "] = company
    clean_data['date'] = date

    second_data.append(clean_data)


for clean_dict in second_data:
    y, m, d = clean_dict['date'].split('-')
    date = datetime.date(int(y), int(m), int(d))
    new_date = date + relativedelta(months=+4)
    clean_dict['Time to check'] = str(new_date)

for clean_dict in second_data:
    y, m, d = clean_dict['date'].split('-')
    date = datetime.date(int(y), int(m), int(d))
    new_date = date + relativedelta(months=+6)
    clean_dict['Final-date'] = str(new_date)


class Database():
    def __init__(self, ticker, days):
        self.ticker = ticker
        data = yf.download(ticker, start="2020-01-01", end="2020-12-30")
        self.df = pd.DataFrame(data)
        pd.set_option('display.max_columns', None)
        self.df = self.df[-days:]

    def quote(self):
        return self.df



pprint(final_data)

stockname = input("Skriv ticker för bolaget:")

db = Database(stockname, 252)
df = db.quote()
print(df.tail())




pivot_high_1=df['High'][-21:-1].max()
pivot_high_2=df['High'][-55:-22].max()
pivot_low_1=df['Low'][-21:-1].min()
pivot_low_2=df['Low'][-55:-22].min()

A=[df['High'][-21:-1].idxmax(), pivot_high_1]
B=[df['High'][-55:-22].idxmax(), pivot_high_2]

A1=[df['Low'][-21:-1].idxmin(), pivot_low_1]
B1=[df['Low'][-55:-22].idxmin(), pivot_low_2]

x1_high_values = [A[0], B[0]]
y1_high_values = [A[1], B[1]]

x1_low_values = [A1[0], B1[0]]
y1_low_values = [A1[1], B1[1]]




plt.rcParams.update({'font.size': 10})
fig, ax1 = plt.subplots(figsize=(14,7))

ax1.set_ylabel('Price in USD')
ax1.set_xlabel('Date')
ax1.set_title(stockname)
ax1.plot('Adj Close',data=df, label='Close Price', linewidth=0.5, color='blue')



ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='Första motståndslinjen', alpha=0.2)
ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='Första supportlinjen', alpha=0.2)
trans = transforms.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
ax1.text(0,pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans,ha="right", va="center")
ax1.text(0,pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans,ha="right", va="center")

ax1.legend()
ax1.grid()
plt.show()
