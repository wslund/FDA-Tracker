import json
import yfinance as yf
from stock_updating import stock_update
import pandas as pd
import time




def update_ticker():
    fileObject = open("Ticker_info.json", "r")
    jsonContent = fileObject.read()
    json_list = json.loads(jsonContent)

    text_to_dicord = []
    file_path = []

    for count, i in enumerate(json_list["Ticker_info"]):
        pdufa = i["pdufa"]
        company = i["company"]
        ticker = i["ticker"]
        resistance = i["resistance"]
        support = i["support"]
        data = yf.download(ticker)
        df = pd.DataFrame(data)

        price = float(df["Close"][-1])
        price = round(price, 2)
        if price > resistance:
            code_number = 1
            text, img = stock_update(company=company, ticker=ticker, pdufa=pdufa, code_number=code_number, element=count)
            text_to_dicord.append(text)
            file_path.append(img)
            time.sleep(2)

        elif price < support:
            code_number = 0
            text, img = stock_update(company=company, ticker=ticker, pdufa=pdufa, code_number=code_number, element=count)
            text_to_dicord.append(text)
            file_path.append(img)
            time.sleep(2)
        else:
            pass

    return text_to_dicord, file_path





