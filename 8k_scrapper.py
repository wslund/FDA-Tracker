import json
from pprint import pprint
import datetime
from dateutil.relativedelta import relativedelta
import requests






url = "https://efts.sec.gov/LATEST/search-index"
form = {"q":"\"pdufa\" \"goal date\" ","dateRange":"custom","startdt":"2020-09-01","enddt":"2020-10-08","category":"all","locationType":"located","locationCode":"all","filter_forms":"8-K","page":"1","from":0}
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
    clean_data["company name and ticker: "] = company
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
    clean_dict['final-date'] = str(new_date)




pprint(final_data)
