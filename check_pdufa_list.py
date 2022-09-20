import json
import datetime


def delete_duplicates():
    new_data = []
    with open("PDUFA.json", 'r') as fp:
        data = json.load(fp)

    for i in data["PDUFA"]:
        status = i["status"]
        company = i["company"]
        ticker = i["ticker"]
        pdufa = i["pdufa"]
        new_data.append((status, company, ticker, pdufa))

    remove_duplicate = tuple(set(new_data))

    pdufa_dict = {"PDUFA": []}

    for i in remove_duplicate:
        status = i[0]
        company = i[1]
        ticker = i[2]
        pdufa = i[3]

        to_dict = {"status": status,
                   "company": company,
                   "ticker": ticker,
                   "pdufa": pdufa}
        pdufa_dict["PDUFA"].append(to_dict)



    with open("PDUFA.json", 'w') as f:
        json.dump(pdufa_dict, f, indent=4)

    return

def remove_passed_dates():
    filepath = 'PDUFA.json'
    with open(filepath, 'r') as fp:
        data = json.load(fp)

    new_data = []

    currentDateTime = datetime.datetime.now()
    date_now = currentDateTime.date()

    for i in data['PDUFA']:
        status = i["status"]
        pdufa = i['pdufa']
        format = "%Y-%m-%d"
        pdufa_date = datetime.datetime.strptime(pdufa, format)
        pdufa_date = pdufa_date.date()
        company = i["company"]
        ticker = i["ticker"]
        if pdufa_date < date_now:
            pass

        else:
            new_data.append((status, company, ticker, pdufa))

    remove_duplicate = tuple(set(new_data))

    pdufa_dict = {"PDUFA": []}

    for i in remove_duplicate:
        status = i[0]
        company = i[1]
        ticker = i[2]
        pdufa = i[3]

        to_dict = {"status": status,
                   "company": company,
                   "ticker": ticker,
                   "pdufa": pdufa}
        pdufa_dict["PDUFA"].append(to_dict)

    with open("PDUFA.json", 'w') as f:
        json.dump(pdufa_dict, f, indent=4)

    return


























