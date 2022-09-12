import json
import datetime





def remove_passed_dates_ticker_info():
    filepath = 'Ticker_info.json'
    with open(filepath, 'r') as fp:
        data = json.load(fp)

    new_data = []

    currentDateTime = datetime.datetime.now()
    date_now = currentDateTime.date()

    for i in data["Ticker_info"]:
        company = i["company"]
        ticker = i["ticker"]
        price = i["price"]
        resistance = i["resistance"]
        support = i["support"]

        pdufa = i['pdufa']
        format = "%Y-%m-%d"
        pdufa_date = datetime.datetime.strptime(pdufa, format)
        pdufa_date = pdufa_date.date()

        if pdufa_date < date_now:
            pass

        else:
            new_data.append((company, ticker, pdufa, price, resistance, support))

    remove_duplicate = tuple(set(new_data))

    pdufa_dict = {"Ticker_info": []}

    for i in remove_duplicate:
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

        pdufa_dict["Ticker_info"].append(to_dict)

    with open("Ticker_info.json", 'w') as f:
        json.dump(pdufa_dict, f, indent=4)

    return


