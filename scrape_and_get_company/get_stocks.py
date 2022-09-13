import json
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms


import datetime
from dateutil.relativedelta import relativedelta






def get_stock(company, ticker, pdufa):
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

    text_to_discord = f'PDUFA for Company: {company}\nTicker: {ticker}\nDate: {pdufa}\nPrice: {price} \nSupport: {support} \nResistance: {resistance}'


    to_dict = {"company": company,
               "ticker": ticker,
               "pdufa": pdufa,
               "price": price,
               "resistance": resistance,
               "support": support}

    write_json(to_dict)


    return text_to_discord, image_filepath

def write_json(new_data, filename='Ticker_info.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data["Ticker_info"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

    return


def changes_status(changes, none_changes):


    status_changes = changes + none_changes


    pdufa_dict = {"PDUFA": []}

    for i in status_changes:
        company = i[0]
        ticker = i[1]
        pdufa = i[2]
        status = i[3]


        to_dict = {"status": status,
                   "company": company,
                   "ticker": ticker,
                   "pdufa": pdufa}

        pdufa_dict["PDUFA"].append(to_dict)



    with open("../json_files/PDUFA.json", 'w') as f:
        json.dump(pdufa_dict, f, indent=4)

    return




def ticker_engine():

    fileObject = open("../json_files/PDUFA.json", "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)

    status_changes = []
    status_changes_none = []
    text_to_discord = []
    img_to_discord = []

    for i in aList["PDUFA"]:
        status = i["status"]
        company = i["company"]
        ticker = i["ticker"]
        pdufa = i["pdufa"]
        if status == True:
            status_changes.append((company, ticker, pdufa, status))

        if status == False:
            text, img = get_stock(company, ticker, pdufa)
            text_to_discord.append(text)
            img_to_discord.append(img)
            status = True
            status_changes.append((company, ticker, pdufa, status))

    changes_status(status_changes, status_changes_none)


    return text_to_discord, img_to_discord















