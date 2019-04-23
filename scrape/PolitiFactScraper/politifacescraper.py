import pandas as pd
import datetime
import requests

from bs4 import BeautifulSoup

months = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}

def find_verdict_datetime(statement):
    #edition = statement.find("p", {"class": "statement__edition"})
    meta = statement.find("span", {"class": "article__meta"})
    date = meta.text.split(',')[1:]
    m_d, year = date
    month, date = m_d.strip().split(" ")
    _date = datetime.date(int(year), months[month.lower()],
                          int(date[:-2]))
    return _date

def find_verdict(statement):
    meter = statement.find_all("div", {"class": "meter"})[0]
    verdict = meter.find_all("a", href=True)[0]
    _verdict = verdict['href'].split('/')[-2]
    _qoute = meter.find('p').text
    return _verdict, _qoute

def find_claim(statement):
    state_body = statement.find("div", {"class": "statement__source"})
    _source = state_body.find("a", href=True).text.strip()

    state_text = statement.find("p", {"class": "statement__text"})
    _claim = state_text.find("a", href=True).text.strip()

    return _source, _claim

def iterate_site(startpage):
    """find the 'next' link and iterate through all sites"""

    page_query = lambda x: "{}?page={}".format(startpage, x)

    page_count = 1

    # fence post loop
    page = requests.get(page_query(page_count))
    soup = BeautifulSoup(page.content, 'html.parser')

    while soup.find("a", {"class": "step-links__next"}):
        # While it has a next button
        page = requests.get(page_query(page_count))
        soup = BeautifulSoup(page.content, 'html.parser')
        page_count += 1
        yield soup

if __name__ == "__main__":

    virginia = "https://www.politifact.com/virginia/statements/"
    west_virginia = "https://www.politifact.com/west-virginia/statements/"

    columns = ['source', 'claim', 'verdict', 'qoute', 'date', 'scrape_date']

    df = pd.DataFrame(columns=columns)

    for soup in iterate_site(west_virginia):
        for statement in soup.find_all("div", {"class": "scoretable__item"}):
            _date = find_verdict_datetime(statement)
            _verdict, _qoute = find_verdict(statement)
            _source, _claim = find_claim(statement)
            df_r = pd.DataFrame([[_source, _claim, _verdict, _qoute, _date,
                                datetime.datetime.utcnow()]], columns=columns)

            df = df.append(df_r)
    # LET's repeat some code hehe :-)
    for soup in iterate_site(virginia):
        for statement in soup.find_all("div", {"class": "scoretable__item"}):
            _date = find_verdict_datetime(statement)
            _verdict, _qoute = find_verdict(statement)
            _source, _claim = find_claim(statement)
            df_r = pd.DataFrame([[_source, _claim, _verdict, _qoute, _date,
                                datetime.datetime.utcnow()]], columns=columns)

            df = df.append(df_r)

    print df.size
    print df.head()
    df.to_csv("./virginia_west_virginia.csv", encoding='utf-8')
