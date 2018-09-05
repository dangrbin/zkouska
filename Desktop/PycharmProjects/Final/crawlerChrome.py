from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import datetime

""" Nastavení Selenia a automatické přihlášení do systému """

def hlavni():
    hodnoty = []
    homeL = []
    awayL = []
    # cap = DesiredCapabilities().FIREFOX
    # cap["marionette"] = False
    options = webdriver.ChromeOptions()
    options.set_headless(headless=True)
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:/chromedriver.exe')
    driver.get("https://betting.vip-ibc.com/login")
    jmeno = driver.find_element_by_name("username")
    heslo = driver.find_element_by_name("password")
    jmeno.clear()
    heslo.clear()
    jmeno.send_keys("VBFuksy")
    heslo.send_keys("H32Wakz87")
    driver.find_element_by_xpath("//button[@type='submit']").click()

    """ Počkání do objevení elementu, poté načtení zdrojového kódu pomocí BeautifulSoup """

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "market-comps")))



    tabulka = {"priceHolder WDW ": [], "priceHolder AsianHandicap ": [],
                        "priceHolder AsianOverUnder ": [], "priceHolder tahou_h ": [], "priceHolder tahou_a ": [],
                        "priceHolder score ": [], "priceHolder cs ": []}

    i = 1
    now = datetime.datetime.now()
    mesic = now.month
    den = now.day
    rok = now.year
    datum = str(den) + ". " + str(mesic) + ". " + str(rok)
    datumF = "vip/" + str(den) + ". " + str(mesic) + ". " + str(rok)
    if not os.path.exists(datumF):
        os.makedirs(datumF)


    while i < 3:
        source = driver.page_source
        sp = BeautifulSoup(source, "html.parser")
        for aktual in sp.find_all("div", class_="market hardwareAcc ir "):
            for price in aktual.find_all("span", {"class": "price"}):
                parent1 = price.parent
                parent2 = parent1.parent.get('class')
                if parent2[0] != "event":
                    pass
                else:
                    hodnoty.append(price)

        print("zahajuji")
        for x in range(0, len(hodnoty)):

            if x % 14 == 0 and x != 0:
                tabulka = {"priceHolder WDW ": [], "priceHolder AsianHandicap ": [],
                           "priceHolder AsianOverUnder ": [], "priceHolder tahou_h ": [],
                           "priceHolder tahou_a ": [],
                           "priceHolder score ": [], "priceHolder cs ": []}
            try:
                hodnota = hodnoty[x].string.strip()
            except AttributeError:
                continue

            typ = hodnoty[x].parent.get('class')
            typF = str(typ[0]) + str(" ") + str(typ[1]) + str(" ")

            tabulka[typF].append(hodnota)
            predek = hodnoty[x].parent
            predekF = predek.parent


            for home in predekF.find_all("span", {"class": "homeTeam"}):
                try:
                    home2 = home.get('title')
                    homeL.append(home2)
                except AttributeError:
                    print("error")

            for away in predekF.find_all("span", {"class": "awayTeam"}):
                try:
                    away2 = away.get('title')
                    awayL.append(away2)
                except AttributeError:
                    print("error")

            homeFF = str.replace(homeL[0], "/", "")
            awayFF = str.replace(awayL[0], "/", "")
            nazev = homeFF + " vs " + awayFF + ".json"

            """
            with open("zkus.json", "r+") as f:
                data = json.load(f)
                data[homeFF] = ""
                data[awayFF] = ""
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()"""

            pokus = "vip/" + datum + "/" + nazev
            if os.path.isfile(pokus):
                pass
            else:
                tab = {"lol": ["jj"]}
                soubor = open(pokus, "w+", encoding="utf-8")
                json.dump(tab, soubor, indent=4)
                soubor.close()

            with open(pokus, "r+") as f:
                data = json.load(f)
                data["sing"] = tabulka
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

            del homeL[:]
            del awayL[:]

        print("hotovo")
        time.sleep(2)
        del hodnoty[:]

