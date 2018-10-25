import bs4 as bs
from selenium import webdriver
import try2



ligy = ["VIE D1", "VIE D2", "ARM D1", "ARM D2", "CZE U19", "CZE U21", "HK D1", "HK PR", "HK D2", "CHA D1", "CHA D2",
        "CHA RL", "CHA CSL", "RUS YthC", "RUS D1", "RUS D2", "RUS D3", "SPA D3", "SPA D4", "ROM D2", "ROM D3",
        "KAZ PR", "KAZ D1", "KAZ D2", "BUL SC", "BUL D1", "BUL D2", "AZE D1", "AZE D1", "UZB D1", "UZB D2", "IDN D1",
        "IDN D2", "GEO D1", "GEO D2", "MOL D1", "MOL D2", "LAT D1", "LAT D2", "POL D1", "POL D2", "MAL D1", "MAL D2"]


def funkce(cislo):

    options = webdriver.ChromeOptions()
    options.set_headless(headless=False)
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:/chromedriver.exe')

    try:
        while True:

            driver.get("http://www.nowgoal.com/")

            source = driver.page_source

            soup = bs.BeautifulSoup(source, "lxml")

            promena = 0
            tabul = []
            konec = ""
            jmena = []

            for all in soup.find_all("span", {"id": "live"}):
                for tr in all.find_all("tr"):
                    promena = 0
                    final = tr.get("id")
                    try:
                        final2 = final.split("_")
                        if final2[0] == "tr1":
                            for td in tr.find_all("td"):
                                fin = td.get("style")
                                try:
                                    fin2 = fin.split(":")
                                    if fin2[0] == "color":
                                        prv = td.contents[0]
                                        konec = prv.contents[0]
                                        for nvm in ligy:
                                            if nvm == konec:
                                                promena = 1

                                except AttributeError:
                                    pass

                            if promena == 1:
                                for tdF in tr.find_all("td"):
                                    cas = tdF.get("id")
                                    try:
                                        cas2 = cas.split("_")
                                        if cas2[0] == "time":
                                            title = tdF.get("title")
                                            if title == "Part1" or title == "Part2":
                                                tabul.append(final2[1])
                                                jmena.append(konec)
                                    except AttributeError:
                                        pass
                    except (AttributeError, IndexError):
                        pass

            # print(tabul)

            for prvek in tabul:
                try2.hlavni(prvek, driver, cislo)

    except KeyboardInterrupt:
        try2.zpravy = []
        vloz = int(input("Zadej:"))
        funkce(vloz)



funkce(3)
