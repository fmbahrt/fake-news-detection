import requests
import threading

from bs4 import BeautifulSoup

class PolitiFactScraper:

    def __init__(self):
        pass

    def start(self):
        pass

def find_verdict(statement):
    meter = statement.find_all("div", {"class": "meter"})[0]
    verdict = meter.find_all("a", href=True)[0]
    verdict = verdict['href'].split('/')[-2]
    qoute = meter.find('p').text
    print verdict, qoute

def find_claim(statement):
    state_body = statement.find("div", {"class": "statement__source"})
    _source = state_body.find("a", href=True).text.strip()

    state_text = statement.find("p", {"class": "statement__text"})
    _claim = state_text.find("a", href=True).text.strip()

    print _source, _claim

if __name__ == "__main__":
    page = requests.get("https://www.politifact.com/west-virginia/statements/")
    soup = BeautifulSoup(page.content, 'html.parser')

    for statement in soup.find_all("div", {"class": "scoretable__item"}):
        #find_verdict(statement)
        find_claim(statement)
    #print statement.find_all("div", {"class": "statement__body"})
