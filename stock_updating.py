import json
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms


import datetime
from dateutil.relativedelta import relativedelta





def stock_update(company, ticker, pdufa, code_number, element):
    days = 252
    currentStartTimeDate = datetime.datetime.now() - relativedelta(months=3)
    currentTimeDate = datetime.datetime.now()
    startDate = currentStartTimeDate.strftime('%Y-%m-%d')
    date = currentTimeDate.strftime('%Y-%m-%d')


    data = yf.download(ticker, start=startDate, end=date)
    df = pd.DataFrame(data)
    pd.set_option('display.max_columns', None)
    df = df[-days:]


    pivot_high_1 = df['High'][-21:-1].max()
    pivot_high_2 = df['High'][-55:-22].max()
    pivot_low_1 = df['Low'][-21:-1].min()
    pivot_low_2 = df['Low'][-55:-22].min()

    A = [df['High'][-21:-1].idxmax(), pivot_high_1]
    B = [df['High'][-55:-22].idxmax(), pivot_high_2]

    A1 = [df['Low'][-21:-1].idxmin(), pivot_low_1]
    B1 = [df['Low'][-55:-22].idxmin(), pivot_low_2]

    x1_high_values = [A[0], B[0]]
    y1_high_values = [A[1], B[1]]

    x1_low_values = [A1[0], B1[0]]
    y1_low_values = [A1[1], B1[1]]

    plt.rcParams.update({'font.size': 10})
    fig, ax1 = plt.subplots(figsize=(16, 7))

    ax1.set_ylabel('USD                         ', loc="top")
    ax1.set_xlabel('Date')
    ax1.set_title(f'{company} ({ticker}) PDUFA: {pdufa}')
    ax1.plot('Adj Close', data=df, label='Close Price', linewidth=0.5, color='blue')

    ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='Resistance', alpha=0.2)
    ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='Support', alpha=0.2)
    trans = transforms.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
    ax1.text(0, pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans, ha="right", va="center")
    ax1.text(0, pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans, ha="right", va="center")

    ax1.legend()
    ax1.grid()
    fig.savefig(f'ticker_images/{company}_{ticker}_{pdufa}.jpg', bbox_inches='tight', dpi=150)

    image_filepath = f'ticker_images/{company}_{ticker}_{pdufa}.jpg'

    price = float(df["Close"][-1])
    price = round(price, 2)

    resistance = float(pivot_high_1)
    resistance = round(resistance, 2)

    support = float(pivot_low_1)
    support = round(support, 2)

    delete_element(element=element)


    to_dict = {"company": company,
               "ticker": ticker,
               "pdufa": pdufa,
               "price": price,
               "resistance": resistance,
               "support": support}


    update_ticker_info(new_dict=to_dict)


    message_return = ""


    if code_number == 1:
        message_return = f'{company}: ({ticker}) : Has broken above the resistance\nNew Price: {price} \nNew Support: {support} \nNew Resistance: {resistance}\nPDUFA: {pdufa}'
    if code_number == 0:
        message_return = f'{company}: ({ticker}) : Has broken support\nNew Price: {price} \nNew Support: {support} \nNew Resistance: {resistance}\nPDUFA: {pdufa}'

    return message_return, image_filepath



def delete_element(element):
    filepath = 'Ticker_info.json'
    with open(filepath, 'r') as fp:
        data = json.load(fp)
    del data["Ticker_info"][element]

    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent=4)

    return

def update_ticker_info(new_dict):
    fileObject = open("Ticker_info.json", "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)

    new_dict = list(new_dict.values())



    old_dict = []
    new_element = []
    for i in aList["Ticker_info"]:
        company = i["company"]
        ticker = i["ticker"]
        pdufa = i["pdufa"]
        price = i["price"]
        resistance = i["resistance"]
        support = i["support"]
        old_dict.append((company, ticker, pdufa, price, resistance, support))


    company_uppdated = new_dict[0]
    ticker_uppdated = new_dict[1]
    pdufa_uppdated = new_dict[2]
    price_uppdated = new_dict[3]
    resistance_uppdated = new_dict[4]
    support_uppdated = new_dict[5]

    new_element.append((company_uppdated, ticker_uppdated, pdufa_uppdated, price_uppdated, resistance_uppdated, support_uppdated))

    merged_list = old_dict + new_element

    ticker_info_dict = {"Ticker_info": []}

    for i in merged_list:
        company = i[0]
        ticker = i[1]
        pdufa = i[2]
        price = i[3]
        resistance = i[4]
        support = i[5]

        to_dict = {"company": company,
                   "ticker": ticker,
                   "pdufa": pdufa,
                   "price": price,
                   "resistance": resistance,
                   "support": support}

        ticker_info_dict['Ticker_info'].append(to_dict)



    with open("Ticker_info.json", 'w') as f:
        json.dump(ticker_info_dict, f, indent=4)

    return




