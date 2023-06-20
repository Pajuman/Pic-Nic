import random
import sys
from random import uniform, randint
import pygame

pygame.mixer.init()

# vyváří karty na základě nested list s vlastnotmi (karty_list) a pocty karet
def generovani_karet(Karta, karty_list, pocty):
    balicek_karet = []
    index = 0
    counter = 0

    for i in range(60):
        balicek_karet.append(Karta((karty_list[index][0]),(karty_list[index][1]),(karty_list[index][2]), (karty_list[index][3]), (karty_list[index][4]), (karty_list[index][4]), (karty_list[index][4])))

        counter += 1

        if pocty[index] == counter:
            index += 1
            counter = 0

    return balicek_karet

# posílá karty vektorem na střed
def posun(hrac, koef_rychlost, vymena_karty, odkud, kam):

    koef_hrac_y = 1 if hrac == "a" else -1
    arc = uniform(-0.5, 0.5)

    # pos_y = 0.2 * koef_hrac * koef_rychlost if kam == "do kose" else 0
    # rotace = uniform(-0.1, 0.1) * koef_rychlost if kam[0: 7] == "do kose" else 0

    if kam == "bal_k1":
        pos_x = -0.3 * koef_rychlost
        pos_y = 0.2 * koef_hrac_y * koef_rychlost
    elif kam == "bal_k2":
        pos_x = 0
        pos_y = 0.2 * koef_hrac_y * koef_rychlost
    elif kam == "bal_k3":
        pos_x = 0.3 * koef_rychlost
        pos_y = 0.2 * koef_hrac_y * koef_rychlost
    elif kam == "bal_a" or kam == "bal_b":
        if odkud == "spec_a_1" or odkud == "spec_b_1":
            pos_x = 0.3 * koef_rychlost * 3
            pos_y = 0
            arc = 0
        elif odkud == "spec_a_2" or odkud == "spec_b_2":
            pos_x = -0.3 * koef_rychlost * 3
            pos_y = 0
            arc = 0
        else:
            pos_x = 0
            pos_y = 0
            arc = koef_rychlost
            kam = vymena_karty

    return [pos_x, pos_y, arc, kam]

# zamíchá vygenerovaný balíček (přesype karty z listu do listu)
def michani(balicek):
    premichany_balicek = []
    while len(balicek) > 0:
        nahoda = randint(0, len(balicek)-1)
        premichany_balicek.append(balicek.pop(nahoda))
    return premichany_balicek

# přemísí karty hráčů tak, aby vrchní karta byla vždy na stejném místě
def prerovnani(balicek, hrac, x, y):

    koef = 1 if hrac == "a" else -1

    for i in range(len(balicek)):
        odstup = 2
        prep_x = x - (len(balicek)-1) * odstup
        prep_y = y - (len(balicek)-1) * odstup * koef
        balicek[i].xx = prep_x + odstup * i
        balicek[i].yy = prep_y + odstup * i * koef
    return balicek

# vyhodnocení na konci hry
def vyhodnoceni (bal_1, bal_2, bal_3, specialove, pavouk_ciha_a, pavouk_ciha_b):
# [balíček, hráč, score] - kdo má v jakém balíčku jaké score
    score_1a = [0, "a", 0]
    score_2a = [1, "a", 0]
    score_3a = [2, "a", 0]
    score_1b = [0, "b", 0]
    score_2b = [1, "b", 0]
    score_3b = [2, "b", 0]

    SCORE = [score_1a, score_2a, score_3a, score_1b, score_2b, score_3b]
    BALICKY = [bal_1, bal_2, bal_3]

# vyhodnocování košíků; kosik = balicek; kos je jeho pořadí 0-2
    for kos in range(3):
        kosik = BALICKY[kos]

        # vyhodnocení jednoho košíku - všechny karty (první a poslední jsou fiktivní)
        for poradi_bal in range(1,len(kosik)):
            hrac = ""
            body = 0
            if kosik[poradi_bal] in specialove:
                [hrac, body] = special_vyhodnoceni(kosik, poradi_bal, specialove)

            # nezamáčknutý hmyzák (ham)
            elif kosik[poradi_bal].typ =="ham" and kosik[poradi_bal+1].typ !="bum":
                # body
                body = kosik[poradi_bal].body
                if kosik[poradi_bal-1].typ =="mnam": body += kosik[poradi_bal-1].body
                hrac = kosik[poradi_bal].hrac

            # přičtení bodů do správného score (košík a hráč)
            for score in SCORE:
                # nastražený pavouk
                # if pavouk_ciha_a == True and kosik[poradi_bal].hrac == "b":
                #     kosik[poradi_bal].hrac = "a"
                #     pavouk_ciha_a = False
                # elif pavouk_ciha_b == True and kosik[poradi_bal].hrac == "a":
                #     kosik[poradi_bal].hrac = "b"
                #     pavouk_ciha_b = False

                    # vyhodnoceni
                if hrac == score[1] and kos == score[0]:
                    score[2] += body



        # vyhodnocení poslední karty chybí!!!!


    return [score_1a, score_1b, score_2a, score_2b, score_3a, score_3b]

# AI :)
def bot (vlastni, b1, b2, b3, AI_int):
    # vrchni_karta karty ze 3 kosiku se zamichaji a vlozi se do "poradi_bal"
    # berou se postupně karty v tomto "poradi_bal" a porovnávají s botovou kartou
    # první vhodný tah se vloží do "odpovedi", takže tam budou 4 odpovědi
    # z odpovědí se vylosuje náhodná odpověď

    smaze = [0, 1, 2]
    poradi_bal = []
    vrchni_karta = [b1, b2, b3]
    odpovedi = ["leva", "stred", "prava", "navrch", "dospod", "spec1", "spec2"]

    while len(smaze) > 0:
        nahoda = random.randint(0, len(smaze)-1)
        poradi_bal.append(smaze.pop(nahoda))

    if vlastni.typ == "bum":
        for i in poradi_bal:
            if vrchni_karta[i].typ == "ham" and vrchni_karta[i].hrac == "a":
                for j in range(AI_int):
                    odpovedi.append(odpovedi[i])

    elif vlastni.typ == "ham":
        for i in poradi_bal:
            if vrchni_karta[i].typ == "mnam":
                for j in range(AI_int):
                    odpovedi.append(odpovedi[i])

    elif vlastni.typ == "mnam":
        for i in poradi_bal:
            if vrchni_karta[i].typ == "ham" and vrchni_karta[i].hrac == "b":
                for j in range(AI_int):
                    odpovedi.append(odpovedi[i])

    # proč???
    if len(odpovedi) ==3:
        odpovedi.append(odpovedi[poradi_bal[0]])

    odpoved = odpovedi[random.randint(0, len(odpovedi)-1)]

    return odpoved

def zvuky (polozena, lezici):
    posmech1 = pygame.mixer.Sound("MP3/posmech1.wav")
    posmech2 = pygame.mixer.Sound("MP3/posmech2.wav")
    posmech3 = pygame.mixer.Sound("MP3/posmech3.wav")
    plac1 = pygame.mixer.Sound("MP3/smack1.mp3")
    plac2 = pygame.mixer.Sound("MP3/smack2.wav")
    plac3 = pygame.mixer.Sound("MP3/smack3.wav")
    posmech = [posmech1, posmech2, posmech3]
    plac = [plac1, plac2, plac3]

    index = random.randint(0,2)
    if polozena.typ == "bum" and lezici.typ == "ham":
        pygame.mixer.stop()
        plac[index].play()
    elif polozena.typ == "ham" and lezici.typ == "mnam":
        pygame.mixer.stop()
        posmech[index].play()


def konec ():
    konec = pygame.mixer.Sound("MP3/chipmank_joy.wav")
    pygame.mixer.stop()
    konec.play()

def special_vyhodnoceni (kosik, poradi_bal, specialove):
    hrac = ""
    body = 0
# KUDLANKA
    if kosik[poradi_bal] == specialove[0] or kosik[poradi_bal] ==specialove[1]:
    # body pro kudlanku
        if kosik[poradi_bal + 1].typ != "bum":
            body = kosik[poradi_bal - 1].body
            hrac = kosik[poradi_bal].hrac
    # je-li kudlanka zaplácnutá, tak může přežít hmyzák pod ní
        elif kosik[poradi_bal + 1].typ == "bum" and kosik[poradi_bal - 1].typ == "ham":
        # když zachráněný hmyzák něco snědl
            body = kosik[poradi_bal - 1].body
            hrac = kosik[poradi_bal - 1].hrac
            if kosik[poradi_bal - 2].typ == "mnam": body += kosik[poradi_bal - 2].body

# # PAVOUK
#     elif kosik[poradi_bal].surf == ("sp_pavouk_a" or "sp_pavouk_b") and kosik[poradi_bal + 1].typ != "plac":
#         if kosik[poradi_bal].hrac == "a": pavouk_ciha_a = True
#         else: pavouk_ciha_b = True
#         if kosik[poradi_bal - 1].typ == "mnam": body = kosik[poradi_bal - 1].body
#         hrac = kosik[poradi_bal].hrac
#
# # CERV
#     elif (kosik[poradi_bal].surf == "sp_cerv_a" or "sp_cerv_b") and kosik[poradi_bal + 1].typ != "plac":
#         if kosik[poradi_bal - 1].typ == "mnam": body = 3 * kosik[poradi_bal - 1].body
#         hrac = kosik[poradi_bal].hrac

# BERUSKA
    elif (kosik[poradi_bal] == specialove[2] or kosik[poradi_bal] == specialove[3]) and kosik[poradi_bal + 1].typ != "bum":
        body = kosik[poradi_bal].body
        if kosik[poradi_bal - 1].typ == "mnam": body += kosik[poradi_bal - 1].body
        hrac = kosik[poradi_bal].hrac

    return [hrac, body]




