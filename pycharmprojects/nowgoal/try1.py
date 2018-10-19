import urllib.request
import bs4 as bs
from selenium import webdriver
import time
import try2

# sauce = urllib.request.urlopen('https://gm.ifortuna.cz/sazeni/fotbal?filter=today').read()

ligy = ["VIE D1", "VIE D2", "ARM D1", "ARM D2", "CZE U19", "CZE U21", "HK D1", "HK PR", "HK D2", "CHA D1", "CHA D2",
        "CHA RL", "CHA CSL", "RUS YthC", "RUS D1", "RUS D2", "RUS D3", "SPA D3", "SPA D4", "ROM D2", "ROM D3",
        "KAZ PR", "KAZ D1", "KAZ D2", "BUL SC", "BUL D1", "BUL D2", "AZE D1", "AZE D1", "UZB D1", "UZB D2", "IDN D1",
        "IDN D2", "GEO D1", "GEO D2", "MOL D1", "MOL D2", "LAT D1", "LAT D2", "POL D1", "POL D2", "MAL D1", "MAL D2"]

options = webdriver.ChromeOptions()
options.set_headless(headless=False)
driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:/chromedriver.exe')
driver.get("http://www.nowgoal.com/")

source = driver.page_source

soup = bs.BeautifulSoup(source, "lxml")

tabul = []

for all in soup.find_all("span", {"id": "live"}):
    for tr in all.find_all("tr"):
        for td in tr.find_all("td"):
            fin = td.get("title")
        final = tr.get("id")
        try:
            final2 = final.split("_")
            if final2[0] == "tr1":
                tabul.append(final2[1])
        except (AttributeError, IndexError):
            pass

print(tabul)

for prvek in tabul:
    try2.hlavni(prvek, driver)


