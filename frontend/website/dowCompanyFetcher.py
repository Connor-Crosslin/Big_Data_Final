import requests
from bs4 import BeautifulSoup

def dowFetcher():
    URL = "https://stockanalysis.com/list/dow-jones-stocks/"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find_all("tr")

    companyNameTexts = {}

    index = 0
    for job_element in results:
        companyName = job_element.find("a")
        if companyName == None:
            continue
        companyNameTexts[index] = companyName.text
        index +=1

    return companyNameTexts