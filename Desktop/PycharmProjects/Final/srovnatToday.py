"""
Dořešit problém s diakritikou
Dořešit to cyklování live

"""

import os
import json
import datetime
from pathlib import Path
import time
import difflib
import fbchat
import json.decoder

promena = 2


def hlavni(hod):
    tab = []
    pole = []
    pole2 = []
    now = datetime.datetime.now()
    mesic = now.month
    den = now.day
    rok = now.year
    datum = str(den) + ". " + str(mesic) + ". " + str(rok)
    i = 2
    cislo = 1
    client = fbchat.Client('neo712@seznam.cz', 'mrpythoner1')
    group = client.searchForGroups("skupina")
    group_Skupina = group[0]



    time.sleep(12)

    while i < 3:
        for file in os.listdir("vip/" + datum):

            if promena == 3:
                return

            del pole[:]
            del pole2[:]
            dataN = {}
            dataP = {}


            string1 = file

            for file2 in os.listdir("fortuna/" + datum):
                string2 = file2
                pocet = 0
                rat = difflib.SequenceMatcher(None, string1, string2).ratio()
                print(rat)
                if rat > 0.7:
                    print(file + " vs " + file2)
                    vip = "vip/" + datum + "/" + file
                    fortuna = "fortuna/" + datum + "/" + file2
                    try:
                        soubor = open(vip, 'r')
                        data1 = json.load(soubor)
                    except json.decoder.JSONDecodeError:
                        time.sleep(0.5)
                        soubor = open(vip, 'r')
                        data1 = json.load(soubor)

                    try:
                        soubor1 = open(fortuna, 'r')
                    except FileNotFoundError:
                        print("Not found:" + file2)
                        continue
                    try:
                        data2 = json.load(soubor1)
                        #print(file + "  " + str(data2))
                    except json.decoder.JSONDecodeError:
                        time.sleep(0.5)
                        data2 = json.load(soubor1)

                    hodnota = data1["sing"]["priceHolder WDW "]
                    if len(hodnota) > 3:
                        del hodnota[0:3]

                    try:

                        hodnota1 = float(data2["zapas"]["domaci"][0])
                        hodnota2 = float(data2["zapas"]["remiza"][0])
                        hodnota3 = float(data2["zapas"]["hoste"][0])
                    except (ValueError, IndexError):
                        # print("Error v hodnotě: " + file2)
                        continue

                    try:
                        marze_vip = 1 / (1 / float(hodnota[0]) + 1 / float(hodnota[1]) + 1 / float(hodnota[2]))
                        marze_fortuna = 1 / (1 / hodnota1 + 1 / hodnota2 + 1 / hodnota3)
                    except IndexError:
                        print("index:" + str(file))
                        continue

                    tab.append(hodnota1)
                    tab.append(hodnota2)
                    tab.append(hodnota3)
                    soubor.close()
                    soubor1.close()

                    for b in range(0, len(hodnota)):

                        if b == 0:
                            if hodnota[0] == "" or hodnota1 == "":
                                print("Chyba!")
                                continue

                            if float(hodnota[0]) > 5 or hodnota1 > 5:
                                pass

                            else:
                                try:
                                    if float(hodnota[0]) > hodnota1:
                                        vysledek = float(hodnota[0]) / hodnota1
                                    else:
                                        vysledek = hodnota1 / float(hodnota[0])
                                except ValueError:
                                    continue

                                if vysledek > hod:
                                    # win32api.MessageBox(0, str(hodnota[0]) + " a " + str(hodnota1), file)
                                    cesta = "hodnotaNad/aktualne/" + file
                                    if os.path.isfile(cesta):
                                        pass
                                    else:
                                        tab2 = {}
                                        soubor3 = open(cesta, "w+", encoding="utf-8")
                                        json.dump(tab2, soubor3, indent=4)
                                        soubor3.close()
                                        zprava = file + ": rozdíl domácí " + str(round(vysledek, 2)) + ", VIP: " + \
                                                 str(hodnota[0]) + ", Fortuna: " + str(hodnota1) + ", Marže Fortuna: " + \
                                                 str(round(marze_fortuna, 3)) + ", Marže VIP: " + str(round(marze_vip, 3))

                                        sent = client.send(fbchat.Message(text=zprava),
                                                           thread_id=group_Skupina.uid, thread_type=fbchat.ThreadType.GROUP)

                                        if sent:
                                            print("Message sent successfully!")
                                        pocet = 1

                                    dat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    dataN["cas"] = str(dat)
                                    dataN["rozdil domaci"] = str(round(vysledek, 2))

                        elif b == 1:
                            if hodnota[1] == "" or hodnota2 == "":
                                print("Chyba!")
                                continue

                            if hodnota2 > 5 or float(hodnota[1]) > 5:
                                pass

                            else:
                                try:
                                    if float(hodnota[1]) > hodnota2:
                                        vysledek = float(hodnota[1]) / hodnota2
                                    else:
                                        vysledek = hodnota2 / float(hodnota[1])
                                except ValueError:
                                    continue

                                if vysledek > hod:
                                    # win32api.MessageBox(0, str(hodnota[1]) + " a " + str(hodnota2), file)

                                    cesta = "hodnotaNad/aktualne/" + file
                                    if os.path.isfile(cesta):
                                        pass
                                    else:
                                        tab2 = {}
                                        soubor3 = open(cesta, "w+", encoding="utf-8")
                                        json.dump(tab2, soubor3, indent=4)
                                        soubor3.close()
                                        zprava = file + ": rozdíl remíza " + str(round(vysledek, 2)) + ", VIP: " + \
                                                 str(hodnota[1]) + ", Fortuna: " + str(hodnota2) + ", Marže Fortuna: " + \
                                                 str(round(marze_fortuna, 3)) + ", Marže VIP: " + str(round(marze_vip, 3))
                                        sent = client.send(fbchat.Message(text=zprava),
                                                           thread_id=group_Skupina.uid, thread_type=fbchat.ThreadType.GROUP)

                                        if sent:
                                            print("Message sent successfully!")
                                        pocet = 2

                                    if pocet == 1:
                                        zprava = file + ": rozdíl remíza " + str(round(vysledek, 2)) + ", VIP: " + \
                                                 str(hodnota[1]) + ", Fortuna: " + str(hodnota2) + ", Marže Fortuna: " + \
                                                 str(round(marze_fortuna, 3)) + ", Marže VIP: " + str(round(marze_vip, 3))
                                        sent = client.send(fbchat.Message(text=zprava),
                                                           thread_id=group_Skupina.uid, thread_type=fbchat.ThreadType.GROUP)

                                        if sent:
                                            print("Message sent successfully!")
                                        pocet = 2

                                    dat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    dataN["cas"] = str(dat)
                                    dataN["rozdil remiza"] = str(round(vysledek, 2))

                        elif b == 2:
                            if hodnota[2] == "" or hodnota3 == "":
                                print("Chyba!")
                                continue

                            if hodnota3 > 5 or float(hodnota[2]) > 5:
                                pass

                            else:
                                try:
                                    if float(hodnota[2]) > hodnota3:
                                        vysledek = float(hodnota[2]) / hodnota3
                                    else:
                                        vysledek = hodnota3 / float(hodnota[2])
                                except ValueError:
                                    continue

                                if vysledek > hod:
                                    # win32api.MessageBox(0, str(hodnota[2]) + " a " + str(hodnota3), file)
                                    cesta = "hodnotaNad/aktualne/" + file
                                    if os.path.isfile(cesta):
                                        pass
                                    else:
                                        tab2 = {}
                                        soubor3 = open(cesta, "w+", encoding="utf-8")
                                        json.dump(tab2, soubor3, indent=4)
                                        soubor3.close()
                                        zprava = file + ": rozdíl hosté " + str(round(vysledek, 2)) + ", VIP: " + \
                                                 str(hodnota[2]) + ", Fortuna: " + str(hodnota3) + ", Marže Fortuna: " + \
                                                 str(round(marze_fortuna, 3)) + ", Marže VIP: " + str(round(marze_vip, 3))
                                        sent = client.send(fbchat.Message(text=zprava),
                                                           thread_id=group_Skupina.uid, thread_type=fbchat.ThreadType.GROUP)

                                        if sent:
                                            print("Message sent successfully!")

                                    if pocet == 2 or pocet == 1:
                                        zprava = file + ": rozdíl hosté " + str(round(vysledek, 2)) + ", VIP: " + \
                                                 str(hodnota[2]) + ", Fortuna: " + str(hodnota3) + ", Marže Fortuna: " + \
                                                 str(round(marze_fortuna, 3)) + ", Marže VIP: " + str(round(marze_vip, 3))
                                        sent = client.send(fbchat.Message(text=zprava),
                                                           thread_id=group_Skupina.uid, thread_type=fbchat.ThreadType.GROUP)

                                        if sent:
                                            print("Message sent successfully!")

                                    dat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    dataN["cas"] = str(dat)
                                    dataN["rozdil hoste"] = str(round(vysledek, 2))

                    sbr = Path("hodnotaNad/aktualne/" + file)
                    if sbr.is_file():
                        fl = "hodnotaNad/aktualne/" + file
                        with open(fl, "w") as f:
                            json.dump(dataN, f, indent=4)
                            f.close()

                    del tab[:]
                    # time.sleep(1.5)
                    cislo += 1
        print("Srovnávač jede")


def historie(hod):
    tab = []
    pole = []
    pole2 = []
    now = datetime.datetime.now()
    mesic = now.month
    den = now.day
    rok = now.year
    datum = str(den) + ". " + str(mesic) + ". " + str(rok)
    i = 2
    cislo = 1

    time.sleep(12)

    while i < 3:
        for file in os.listdir("vip/" + datum):
            if promena == 3:
                return

            del pole[:]
            del pole2[:]
            dataN = {}
            dataP = {}

            string1 = file

            for file2 in os.listdir("fortuna/" + datum):
                string2 = file2
                rat = difflib.SequenceMatcher(None, string1, string2).ratio()
                if rat > 0.7:

                    vip = "vip/" + datum + "/" + file
                    fortuna = "fortuna/" + datum + "/" + file2
                    try:
                        soubor = open(vip, 'r')
                        data1 = json.load(soubor)
                    except json.decoder.JSONDecodeError:
                        time.sleep(0.5)
                        soubor = open(vip, 'r')
                        data1 = json.load(soubor)

                    try:
                        soubor1 = open(fortuna, 'r')
                    except FileNotFoundError:
                        print("Not found:" + file2)
                        continue
                    try:
                        data2 = json.load(soubor1)
                    except json.decoder.JSONDecodeError:
                        time.sleep(0.5)
                        data2 = json.load(soubor1)

                    hodnota = data1["sing"]["priceHolder WDW "]
                    if len(hodnota) > 3:
                        del hodnota[0:3]

                    try:
                        hodnota1 = float(data2["zapas"]["domaci"][0])
                        hodnota2 = float(data2["zapas"]["remiza"][0])
                        hodnota3 = float(data2["zapas"]["hoste"][0])
                    except (ValueError, IndexError):
                        # print("Error v hodnotě: " + file2)
                        continue

                    tab.append(hodnota1)
                    tab.append(hodnota2)
                    tab.append(hodnota3)
                    soubor.close()
                    soubor1.close()

                    for b in range(0, len(hodnota)):
                        if b == 0:
                            if hodnota[0] == "" or hodnota1 == "":
                                print("Chyba!")
                                continue

                            if float(hodnota[0]) > 5 or hodnota1 > 5:
                                pass
                            else:

                                try:
                                    if float(hodnota[0]) > hodnota1:
                                        vysledek = float(hodnota[0]) / hodnota1
                                    else:
                                        vysledek = hodnota1 / float(hodnota[0])
                                except ValueError:
                                    continue

                                if vysledek > hod:
                                    dat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    dataN["cas"] = str(dat)
                                    dataN["rozdil domaci"] = str(round(vysledek, 2))

                                    pole.append(hodnota[0])
                                    pole.append(hodnota[1])
                                    try:
                                        pole.append(hodnota[2])
                                    except IndexError:
                                        print("Index:" + file)
                                        time.sleep(0.5)
                                        pole.append(hodnota[2])

                                    pole2.append(hodnota1)
                                    pole2.append(hodnota2)
                                    pole2.append(hodnota3)
                                    if os.path.isfile("hodnotaNad/kratkaH/" + file):
                                        pass
                                    else:
                                        tab2 = {}
                                        soubor2 = open("hodnotaNad/kratkaH/" + file, "w+", encoding="utf-8")
                                        json.dump(tab2, soubor2, indent=4)
                                        soubor2.close()

                        elif b == 1:
                            if hodnota[1] == "" or hodnota2 == "":
                                print("Chyba!")
                                continue

                            if float(hodnota[1]) > 5 or hodnota2 > 5:
                                pass
                            else:

                                try:
                                    if float(hodnota[1]) > hodnota2:
                                        vysledek = float(hodnota[1]) / hodnota2
                                    else:
                                        vysledek = hodnota2 / float(hodnota[1])
                                except ValueError:
                                    continue

                                if vysledek > hod:
                                    dat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    dataN["cas"] = str(dat)
                                    dataN["rozdil remiza"] = str(round(vysledek, 2))

                                    if len(pole) == 0:
                                        pole.append(hodnota[0])
                                        pole.append(hodnota[1])
                                        try:
                                            pole.append(hodnota[2])
                                        except IndexError:
                                            print("Index:" + file)
                                        pole2.append(hodnota1)
                                        pole2.append(hodnota2)
                                        pole2.append(hodnota3)
                                        if os.path.isfile("hodnotaNad/kratkaH/" + file):
                                            pass
                                        else:
                                            tab2 = {}
                                            soubor2 = open("hodnotaNad/kratkaH/" + file, "w+", encoding="utf-8")
                                            json.dump(tab2, soubor2, indent=4)
                                            soubor2.close()
                                    else:
                                        pass

                        elif b == 2:
                            if hodnota[2] == "" or hodnota3 == "":
                                print("Chyba!")
                                continue

                            if float(hodnota[2]) > 5 or hodnota3 > 5:
                                pass
                            else:

                                try:
                                    if float(hodnota[2]) > hodnota3:
                                        vysledek = float(hodnota[2]) / hodnota3
                                    else:
                                        vysledek = hodnota3 / float(hodnota[2])
                                except ValueError:
                                    continue

                                if vysledek > hod:
                                    dat = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    dataN["cas"] = str(dat)
                                    dataN["rozdil hoste"] = str(round(vysledek, 2))

                                    if len(pole) == 0:
                                        pole.append(hodnota[0])
                                        pole.append(hodnota[1])
                                        try:
                                            pole.append(hodnota[2])
                                        except IndexError:
                                            print("Index:" + file)
                                            time.sleep(5)

                                        pole2.append(hodnota1)
                                        pole2.append(hodnota2)
                                        pole2.append(hodnota3)
                                        if os.path.isfile("hodnotaNad/kratkaH/" + file):
                                            pass
                                        else:
                                            tab2 = {}
                                            soubor2 = open("hodnotaNad/kratkaH/" + file, "w+", encoding="utf-8")
                                            json.dump(tab2, soubor2, indent=4)
                                            soubor2.close()

                    sbr2 = Path("hodnotaNad/kratkaH/" + file)
                    if sbr2.is_file():
                        fl = "hodnotaNad/kratkaH/" + file
                        with open(fl, "r+") as f:
                            data = json.load(f)
                            data[cislo] = pole
                            data[cislo + 1] = pole2
                            f.seek(0)
                            json.dump(data, f, indent=4)
                            f.truncate()
                            f.close()
                            cislo += 2

                    del tab[:]
                    # time.sleep(1.5)

        time.sleep(30)
        print("Historie jede")
