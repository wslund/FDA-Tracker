import json
import yfinance as yf
from datetime import datetime


from stock_updating import stock_update


def ticker_update():
    fileObject = open("Ticker_info.json", "r")
    jsonContent = fileObject.read()
    json_list = json.loads(jsonContent)

    ticker_list = []

    for i in json_list["Ticker_info"]:
        pdufa = i["pdufa"]
        company = i["company"]
        ticker = i["ticker"]
        resistance = i["resistance"]
        support = i["support"]
        ticker_list.append((ticker, resistance, support))
        data = yf.download(ticker, start=datetime.now())
        price = data["Close"]
        price = price[0]
        if price > resistance:
            stock_update(company=company, ticker=ticker, pdufa=pdufa)
        elif price < support:
            stock_update(company=company, ticker=ticker, pdufa=pdufa)
        else:
            pass
    return




