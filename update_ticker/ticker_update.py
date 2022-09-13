import json
import yfinance as yf
from scrape_and_get_company.stock_updating import stock_update

import datetime
from datetime import datetime


def update_ticker():
    fileObject = open("../json_files/Ticker_info.json", "r")
    jsonContent = fileObject.read()
    json_list = json.loads(jsonContent)

    text_to_dicord = ""
    file_path = ""

    for count, i in enumerate(json_list["Ticker_info"]):
        pdufa = i["pdufa"]
        company = i["company"]
        ticker = i["ticker"]
        resistance = i["resistance"]
        support = i["support"]
        data = yf.download(ticker, start=datetime.now())
        price = data["Close"]
        price = price[0]
        if price > resistance:
            code_number = 1
            text, img = stock_update(company=company, ticker=ticker, pdufa=pdufa, code_number=code_number, element=count)
            text_to_dicord = text
            file_path = img

        elif price < support:
            code_number = 0
            text, img = stock_update(company=company, ticker=ticker, pdufa=pdufa, code_number=code_number, element=count)
            text_to_dicord = text
            file_path = img
        else:
            pass
    return text_to_dicord, file_path







