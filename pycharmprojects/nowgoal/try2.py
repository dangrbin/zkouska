import urllib.request
import bs4 as bs
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# sauce = urllib.request.urlopen('http://data.nowgoal.com/3in1odds/24_1629398.html').read()


def hlavni(adresa, driver, cislo):
    """
    options = webdriver.ChromeOptions()
    options.set_headless(headless=False)
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:/chromedriver.exe')"""

    driver.get("http://data.nowgoal.com/3in1odds/24_" + adresa + ".html")

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "div_d")))

    source = driver.page_source

    soup = bs.BeautifulSoup(source, "lxml")

    pocet = 0
    pocet2 = 7
    tabulka = []
    spravne = ""
    nazvy = []

    poc = 0
    for h4 in soup.find_all("h4"):
        if poc == 1:
            for nazev1 in h4.find_all("font"):
                nazvy.append(nazev1.text)
        poc += 1

    for every in soup.find_all("div", {"id": "div_d"}):
        for td in every.find_all("td"):
            if pocet < 10:
                pass
            else:
                if pocet2 % 7 == 0:
                    get = td.get("style")
                    tabulka.append(get)
                else:
                    pass
                pocet2 += 1

            pocet += 1

    tabulka_n = []

    for kazdy in tabulka:
        novy = kazdy.split(":")
        tabulka_n.append(novy[1])

    vysledek = "red"
    zelena = 0

    for prvek in tabulka_n:

        if prvek == "red;":
            zelena = 0

        if prvek == "green;":
            zelena += 1

        if zelena == cislo:
            print("Zelená!" + str(nazvy[0] + " vs " + str(nazvy[1])))
            zelena = 0

