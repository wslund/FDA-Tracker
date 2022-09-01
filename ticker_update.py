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
            text1 = f'{company}: {ticker} Has broken above the resistance'
            stock_update(company=company, ticker=ticker, pdufa=pdufa, message=text1)
        elif price < support:
            text2 = f'{company}: {ticker} Has broken support'
            stock_update(company=company, ticker=ticker, pdufa=pdufa, message=text2)
        else:
            pass
    return




