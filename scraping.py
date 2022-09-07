import requests
from bs4 import BeautifulSoup
import json
import datetime
import time


def get_url():
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    date = str(date)

    URL_list = []
    url = "https://efts.sec.gov/LATEST/search-index"
    form = {"q": "\"pdufa goal date of\" ", "dateRange": "custom", "startdt": "2021-12-12", "enddt": date,
            "category": "all", "locationType": "located", "locationCode": "all", "filter_forms": "8-K", "page": "1",
            "from": 0}
    form_data = json.dumps(form)
    result = requests.post(url, data=form_data).text

    company_list = []
    ticker_list = []
    for d in json.loads(result)['hits']['hits']:
        adsh = d['_source']['adsh'].replace("-", "")
        ciks = d['_source']['ciks']
        ciks = ciks[0]
        id = d['_id'].split(":")
        id = id[1]
        doc_url = f'https://www.sec.gov/Archives/edgar/data/{ciks}/{adsh}/{id}'
        URL_list.append(doc_url)

        tick = d['_source']['display_names']
        tick = str(tick)
        tick = tick.replace(f'(CIK {ciks})', "")
        char1 = '('
        char2 = ')'
        ticker = tick[tick.find(char1) + 1: tick.find(char2)]
        ticker = ticker.split(",")
        ticker = ticker[0]

        comp = d['_source']['display_names']
        comp = str(comp)
        comp = comp.split()

        company = comp[0]

        company = company.replace("[", "").replace("'", "")
        ticker_list.append(ticker)
        company_list.append(company)
        time.sleep(1)



    return URL_list, ticker_list, company_list



def scrape_and_remove_tags(URL):
    page = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    page = page.content
    soup = BeautifulSoup(page, "html.parser")

    file = ' '.join(soup.stripped_strings)

    for data in soup(['style', 'script']):
        data.decompose()

    text_file = open("scrape_text", "w", encoding="utf-8")
    n = text_file.write(file)
    text_file.close()
    return



def pick_out_line():
    string1 = '(pdufa) goal date of'
    string2 = 'pdufa goal date of'


    file1 = open("scrape_text", "r", encoding="utf-8")

    flag = 0
    index = 0

    for i in file1:
        line = i.lower()
        index += 1

        if string1 in line:
            flag = 1
            break
        elif string2 in line:
            flag = 1
            break


    if flag == 0:
        print('Not Found')

    file_ = open("scrape_text", encoding="utf-8")

    content = file_.readlines()

    sentence_list = content[index - 1].lower().split()

    i = 0
    pos = -1

    while i < len(sentence_list):
        first = sentence_list[i]
        second = sentence_list[i + 1]
        third = sentence_list[i + 2]
        fourth = sentence_list[i + 3]
        i += 1
        pos += 1
        if first == 'pdufa' and second == 'goal' and third == 'date' and fourth == 'of':
            break
        elif first == '(pdufa)' and second == 'goal' and third == 'date' and fourth == 'of':
            break

    nums = range(pos, pos + 7)
    nums = list(nums)

    first_cleaning = []
    third_cleaning = []

    for i in nums:
        word = sentence_list[i].split()
        first_cleaning.append(word)

    second_cleaning = list(map(''.join, first_cleaning))

    for i in second_cleaning:
        word = i.replace(",", "").replace(".", "")
        third_cleaning.append(word)

    return third_cleaning





def pick_out_month(line):

    months = [("january", 1), ("february", 2), ("march", 3), ("april", 4), ("may", 5), ("june", 6), ("july", 7), ("august", 8), ("september", 9), ("october", 10),
              ("november", 11), ("december", 12)]
    month = ""

    for i in months:
        m = i[0]
        mon = i[1]
        for k in line:
            word = k
            if m == word:
                month = mon
                month = str(month)
                month = month.zfill(2)

    return month

def pick_out_day(line):
    days = range(1, 32)
    days = list(days)
    days = map(str, days)
    days = list(days)

    day = ""


    for i in days:
        d = i
        for k in line:
            word = k
            if d == word:
                day = d
                day = str(day)
                day = day.zfill(2)

    return day.zfill(2)

def pick_out_year(line):
    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    years = date.strftime("%Y")
    years = int(years)


    years = range(years, years + 10)
    years = map(str, years)
    years = list(years)

    year = ""

    for i in years:
        y = i
        for k in line:
            word = k
            if y == word:
                year = y
    return year


def check_list():

    fileObject = open("PDUFA.json", "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)

    check_list = []

    for i in aList["PDUFA"]:
        status = i["status"]
        company = i["company"]
        ticker = i["ticker"]
        pdufa = i["pdufa"]
        check_list.append((status, company, ticker, pdufa))

    check_list = tuple(set(check_list))

    for i in check_list:
        status = i[0]
        company = i[1]
        ticker = i[2]
        pdufa = i[3]

        to_dict = {"satus": status,
                   "company": company,
                   "ticker": ticker,
                   "pdufa": pdufa}

        write_json(to_dict)

    return

def write_json(data_new):

    new_data = []
    old_data = []
    with open("PDUFA.json", 'r') as fp:
        data = json.load(fp)

    for i in data["PDUFA"]:
        status = i["status"]
        company = i["company"]
        ticker = i["ticker"]
        pdufa = i["pdufa"]
        old_data.append((status, company, ticker, pdufa))

    for i in list(data_new):
        status = i["status"]
        company = i["company"]
        ticker = i["ticker"]
        pdufa = i["pdufa"]
        new_data.append((status, company, ticker, pdufa))

    merged_data = new_data + old_data
    remove_duplicate = tuple(set(merged_data))

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


def scrape_engine():


    counter = 0
    URL, ticker, company = get_url()

    company_info = []



    for i in URL:

        scrape_and_remove_tags(i)

        line = pick_out_line()
        month = pick_out_month(line)
        day = pick_out_day(line)
        year = pick_out_year(line)

        comp = company[counter]
        tick = ticker[counter]


        counter += 1
        company_info.append((comp, tick, day, month, year))
        time.sleep(1)



    company_info = tuple(set(company_info))

    new_data = []


    for i in company_info:
        company = i[0]
        ticker = i[1]
        day = i[2]
        month = i[3]
        year = i[4]
        pdufa = f'{year}-{month}-{day}'
        status = False

        to_dict = {"status": status,
                   "company": company,
                   "ticker": ticker,
                   "pdufa": pdufa}

        new_data.append(to_dict)


    write_json(new_data)


    return



test = scrape_engine()














