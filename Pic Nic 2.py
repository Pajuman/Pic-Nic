import sys
sys.path.append("D:\Python\Lib\site-packages")

import pygame
import pynput.keyboard
from pynput.keyboard import Key, Controller

import PN_sub

pygame.mixer.init()

# class karta (hrac, typ, body, surf, arc, xx, yy)
class Karta:
    def __init__(self, hrac, typ, body, surf, arc, xx, yy):
        self.hrac = hrac
        self.typ = typ
        self.body = body
        self.surf = surf
        self.arc = arc
        self.xx = xx
        self.yy = yy

# nulová karta je imaginární karta položená dokaždého ze 3 košíků
nic = pygame.Surface((1, 1))
nul_karta = Karta("a", "nic", 0, nic, 0, 1, 1)

AI = True           # vypíná a zapíná AI
AI_rychlost = 0.2   # koeficient rychlosti pohybu karty
AI_int = 30         # čím vyšší číslo, tím je AI méně náhodná
RYCHLOST = 5        # rychlost celé hry
BAL_AB_X = 543      # poloha blíčků hráčů
BAL_A_Y = 80
BAL_B_Y = 605
MODRA = (20, 20, 140)
CERVENA = (140, 20, 20)

# variables
bal_a = []              # balíčky hráčů a košů
bal_b = []
bal_k1 = [nul_karta]
bal_k2 = [nul_karta]
bal_k3 = [nul_karta]
leti_a = []             # karta v letu hráče a/b
leti_b = []
# balíčky speciálních karet jsou deklarovány později jako spec_a_1, spec_a_2, spec_b_1, spec_b_2

posun_a = [0, 0, 0]     # x, y, natoceni letící karty
posun_b = [0, 0, 0]

povoleni_a = True       # další karta nemůže být hozena,dokud není povolení True
povoleni_b = True

pavouk_ciha_a = False
pavouk_ciha_b = False

body_a = 0
body_b = 0
prubeh_hry = "hraní"    # řídí fázy hry skrze while
keyboard = Controller()

# grafika
screen = pygame.display.set_mode((1200, 800))
trava = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/trava.jpg").convert_alpha(),0, 1.6)
ubrus = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/ubrus.jpg").convert_alpha(),45, 0.21)

mrav_a = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/mravenec_a.png").convert_alpha(), 0, 0.15)
mrav_b = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/mravenec_b.png").convert_alpha(), 0, 0.15)
mou_a = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/moucha_a.png").convert_alpha(), 0, 0.15)
mou_b = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/moucha_b.png").convert_alpha(), 0, 0.15)
plac_a = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/placacka.png").convert_alpha(), 0, 0.15)
plac_b = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/placacka_b.png").convert_alpha(), 0, 0.15)
j1_a = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/jidlo1_a.png").convert_alpha(), 0, 0.15)
j1_b = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/jidlo1_b.png").convert_alpha(), 0, 0.15)
j2_a = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/jidlo2_a.png").convert_alpha(), 0, 0.15)
j2_b = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/jidlo2_b.png").convert_alpha(), 0, 0.15)
j3_a = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/jidlo3_a.png").convert_alpha(), 0, 0.15)
j3_b = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/jidlo3_b.png").convert_alpha(), 0, 0.15)

sp_beru_a = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/beru_a.png").convert_alpha(), 0, 0.15)
sp_kudla_a = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/kudla_a.png").convert_alpha(), 0, 0.15)
sp_beru_b = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/beru_b.png").convert_alpha(), 0, 0.15)
sp_kudla_b = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/kudla_b.png").convert_alpha(), 0, 0.15)

KUDLANKA_A = Karta("a", "bum", 0, sp_kudla_a, 0, 343, 80)
KUDLANKA_B = Karta("b", "bum", 0, sp_kudla_b, 0, 343, 605)
BERUSKA_A = Karta("a", "ham", 4, sp_beru_a, 0, 743, 80)
BERUSKA_B = Karta("b", "ham", 4, sp_beru_b, 0, 743, 605)

spec_a_1 = [KUDLANKA_A]
spec_b_1 = [KUDLANKA_B]
spec_a_2 = [BERUSKA_A]
spec_b_2 = [BERUSKA_B]

specialove = (KUDLANKA_A, KUDLANKA_B, BERUSKA_A, BERUSKA_B)


# tvorba karet
"""definuje všechny karty ///  pocty říkají, kolikrát je která karta v balíčku
     ostatní listy (atributy třídy "karta" se skloubí do nested list - karty_list)"""
pocty = [8, 3, 8, 6, 3, 2]*2

hrac = ["a"]*6 + ["b"]*6
typ = ["ham", "ham", "bum", "mnam", "mnam", "mnam"]*2
body = [1, 2, 0, 1, 2, 3]*2
obrazky = [mrav_a, mou_a, plac_a, j1_a, j2_a, j3_a, mrav_b, mou_b, plac_b, j1_b, j2_b, j3_b]
axy = [0]*12

karty_list = list(zip(hrac, typ, body, obrazky, axy))

# celkový balíček karet -> zamíchá se -> roztřídí do dvou hráčských balíčků -> umístí se na hrací plochu
balicek_karet = PN_sub.generovani_karet(Karta, karty_list, pocty)
balicek_karet = PN_sub.michani(balicek_karet)
for i in balicek_karet:
    if i.hrac == "a":
        bal_a.append(i)
    else:
        bal_b.append(i)

bal_a = PN_sub.prerovnani(bal_a, "a", BAL_AB_X, BAL_A_Y)
bal_b = PN_sub.prerovnani(bal_b, "b", BAL_AB_X, BAL_B_Y)


# průběh hry
# while prubeh_hry == "příprava":
#
#     font_bada = pygame.font.Font("Fonts/BadaBoomCE.otf", 50)
#     font_stand = pygame.font.Font(None, 25)
#
#     # pocet_hracu = font_bada.render(("Vyber počet hráčů"), True, CERVENA)
#     jeden_hrac = font_bada.render("1 hráč", True, MODRA)
#     dva_hraci = font_bada.render("2 hráči", True, MODRA)
#     parchment = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/Parchment.jpg"), 0, 0.4)
#
#
#     screen.blit(parchment, (150, 50))
#     screen.blit(pocet_hracu, (300, 100))
#     screen.blit(jeden_hrac, (350, 170))
#     screen.blit(dva_hraci, (500, 170))
#
#     pygame.event.pump()
#     pygame.init()
#     pygame.display.update()

while prubeh_hry == "hraní":
# variables
    keys = pygame.key.get_pressed()
    ind_a = len(bal_a) -1
    ind_b = len(bal_b) - 1

# povoleni k letu - bez toho nejde hodit další kartu (žádná karta nesmí letět a nesmí být zmáčknutá klávesa)
    if len(leti_a) == 0 and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
        povoleni_a = True
    if len(leti_b) == 0 and not keys[pygame.K_KP4] and not keys[pygame.K_KP5] and not keys[pygame.K_KP6]:
        povoleni_b = True

### AI ### - hráč "b" je AI pokud platí AI = True
    # PN_sub.bot(karta hráče "b", karty na vrších balíčků, AI_int) -> vyhodnotí botem zmáčknutou klávesu
    if AI and povoleni_b:
        if not bal_b and spec_b_1:
            keyboard.tap(pynput.keyboard.KeyCode(vk=103))
        if not bal_b and spec_b_2:
            keyboard.tap(pynput.keyboard.KeyCode(vk=105))

        AI_kam = (PN_sub.bot(bal_b[len(bal_b)-1], bal_k1[len(bal_k1)-1], bal_k2[len(bal_k2)-1], bal_k3[len(bal_k3)-1], AI_int))

        if AI_kam == "leva": keyboard.tap(pynput.keyboard.KeyCode(vk=100))
        elif AI_kam == "stred": keyboard.tap(pynput.keyboard.KeyCode(vk=101))
        elif AI_kam == "prava": keyboard.tap(pynput.keyboard.KeyCode(vk=102))
        elif AI_kam == "navrch": keyboard.tap(pynput.keyboard.KeyCode(vk=104))
        elif AI_kam == "dospod": keyboard.tap(pynput.keyboard.KeyCode(vk=98))
        elif AI_kam == "spec1" and len(spec_b_1)==1 : keyboard.tap(pynput.keyboard.KeyCode(vk=103))
        elif AI_kam == "spec2" and len(spec_b_2)==1: keyboard.tap(pynput.keyboard.KeyCode(vk=105))


# events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# tlačítka

            # hráč "a" pustil tlačítko
        preskocit = False
        if event.type == pygame.KEYUP and povoleni_a == True:
            if event.key == pygame.K_a: vymena_karty, odkud, kam = "ne", "bal_a", "bal_k1"
            elif event.key == pygame.K_s: vymena_karty, odkud, kam = "ne", "bal_a", "bal_k2"
            elif event.key == pygame.K_d: vymena_karty, odkud, kam = "ne", "bal_a", "bal_k3"
            elif event.key == pygame.K_q and len(spec_a_1) == 1: vymena_karty, odkud, kam = "ne", "spec_a_1", "bal_a"
            elif event.key == pygame.K_e and len(spec_a_2) == 1: vymena_karty, odkud, kam = "ne", "spec_a_2", "bal_a"
            elif event.key == pygame.K_w: vymena_karty, odkud, kam = "dospod", "bal_a", "bal_a"
            elif event.key == pygame.K_x: vymena_karty, odkud, kam = "navrch", "bal_a", "bal_a"
            else: preskocit = True

            if not preskocit:
                posun_a = PN_sub.posun("a", RYCHLOST, vymena_karty, odkud, kam)
                odkud = eval(odkud)

                if posun_a[3] == "navrch":
                    leti_a.append(odkud[0])
                    del odkud[0]
                else:
                    leti_a.append(odkud[len(odkud)-1])
                    del odkud[len(odkud)-1]
                povoleni_a = False

            # hráč "b" pustil tlačítko
        preskocit = False
        if event.type == pygame.KEYUP and povoleni_b == True:
            if event.key == pygame.K_KP4: vymena_karty, odkud, kam = "ne", "bal_b", "bal_k1"
            elif event.key == pygame.K_KP5: vymena_karty, odkud, kam = "ne", "bal_b", "bal_k2"
            elif event.key == pygame.K_KP6: vymena_karty, odkud, kam = "ne", "bal_b", "bal_k3"
            elif event.key == pygame.K_KP7 and len(spec_b_1) == 1: vymena_karty, odkud, kam = "ne", "spec_b_1", "bal_b"
            elif event.key == pygame.K_KP9 and len(spec_b_2) == 1: vymena_karty, odkud, kam = "ne", "spec_b_2", "bal_b"
            elif event.key == pygame.K_KP8: vymena_karty, odkud, kam = "dospod", "bal_b", "bal_b"
            elif event.key == pygame.K_KP2: vymena_karty, odkud, kam = "navrch", "bal_b", "bal_b"
            else: preskocit = True

            if preskocit == False:
                posun_b = PN_sub.posun("b", RYCHLOST, vymena_karty, odkud, kam)
                odkud = eval(odkud)

                if posun_b[3] == "navrch":
                    leti_b.append(odkud[0])
                    del odkud[0]
                else:
                    leti_b.append(odkud[len(odkud) - 1])
                    del odkud[len(odkud) - 1]
                povoleni_b = False

# vykreslovani trávy a ubrusu
    ubrus_rect1 = ubrus.get_rect(center=(220, 415))
    ubrus_rect2 = ubrus.get_rect(center=(607, 415))
    ubrus_rect3 = ubrus.get_rect(center=(998, 415))
    screen.blit(trava, (0, 0))
    screen.blit(ubrus, ubrus_rect1)
    screen.blit(ubrus, ubrus_rect2)
    screen.blit(ubrus, ubrus_rect3)

# vykreslování balíčků
    for i in bal_a:
        screen.blit(i.surf, (i.xx, i.yy))
    for i in bal_b:
        screen.blit(i.surf, (i.xx, i.yy))
    for i in bal_k1:
        screen.blit(pygame.transform.rotate(i.surf, i.arc), (i.xx, i.yy))
    for i in bal_k2:
        screen.blit(pygame.transform.rotate(i.surf, i.arc), (i.xx, i.yy))
    for i in bal_k3:
        screen.blit(pygame.transform.rotate(i.surf, i.arc), (i.xx, i.yy))
    for i in spec_a_1:
        screen.blit(i.surf, (i.xx, i.yy))
    for i in spec_a_2:
        screen.blit(i.surf, (i.xx, i.yy))
    for i in spec_b_1:
        screen.blit(i.surf, (i.xx, i.yy))
    for i in spec_b_2:
        screen.blit(i.surf, (i.xx, i.yy))

# vykreslování letící karty hráče "a" a za tím hráče "b"
    for i in leti_a:
        i.xx += posun_a[0]
        i.yy += posun_a[1]
        i.arc += posun_a[2]
        screen.blit(pygame.transform.rotate(i.surf, i.arc), (int(i.xx), int(i.yy)))
    #do kterého balíčku karta přistane
        if posun_a[3] == "bal_a" and 535 < i.xx < 555:
            bal_a.append(i)
            leti_a.clear()
        elif posun_a[3] == "dospod" and i.arc >= 360:
            i.arc = 0
            bal_a.insert(0, i)
            leti_a.clear()
        elif posun_a[3] == "navrch" and i.arc >= 360:
            i.arc = 0
            bal_a.append(i)
            leti_a.clear()

        if i.yy >= 343:
            leti_a.clear()
            if i.xx < BAL_AB_X:
                bal_k1.append(i)
                lezici = bal_k1[len(bal_k1)-2]
            elif i.xx == BAL_AB_X:
                bal_k2.append(i)
                lezici = bal_k2[len(bal_k2) - 2]
            elif i.xx > BAL_AB_X:
                bal_k3.append(i)
                lezici = bal_k3[len(bal_k3) - 2]
        # zvuky po přistání karty
            PN_sub.zvuky(i, lezici)

    for i in leti_b:
        i.xx += posun_b[0]
        i.yy += posun_b[1]
        i.arc += posun_b[2]
        screen.blit(pygame.transform.rotate(i.surf, i.arc), (int(i.xx), int(i.yy)))
        # do kterého balíčku karta přistane
        if posun_b[3] == "bal_b" and 535 < i.xx < 555:
            bal_b.append(i)
            leti_b.clear()
        elif posun_b[3] == "dospod" and i.arc >= 360:
            i.arc = 0
            bal_b.insert(0, i)
            leti_b.clear()
        elif posun_b[3] == "navrch" and i.arc >= 360:
            i.arc = 0
            bal_b.append(i)
            leti_b.clear()

        if i.yy <= 343:
            leti_b.clear()
            if i.xx < BAL_AB_X:
                bal_k1.append(i)
                lezici = bal_k1[len(bal_k1) - 2]
            elif i.xx == BAL_AB_X:
                bal_k2.append(i)
                lezici = bal_k2[len(bal_k2) - 2]
            elif i.xx > BAL_AB_X:
                bal_k3.append(i)
                lezici = bal_k3[len(bal_k3) - 2]

    # zvuky po přistání karty
            PN_sub.zvuky(i, lezici)

    PN_sub.prerovnani(bal_a, "a", BAL_AB_X, BAL_A_Y)
    PN_sub.prerovnani(bal_b, "b", BAL_AB_X, BAL_B_Y)

    #
    # for i in leti_b:
    #     i.xx += posun_b[0]
    #     i.yy += posun_b[1]
    #     i.arc += posun_b[2]
    #     screen.blit(pygame.transform.rotate(i.surf, i.arc), (int(i.xx), int(i.yy)))
    #     if i.yy <= 343:
    #         leti_b.clear()
    #         if i.xx < BAL_AB_X:
    #             bal_k1.append(i)
    #             lezici = bal_k1[len(bal_k1) - 2]
    #         elif i.xx == BAL_AB_X:
    #             bal_k2.append(i)
    #             lezici = bal_k2[len(bal_k2) - 2]
    #         if i.xx > BAL_AB_X:
    #             bal_k3.append(i)
    #             lezici = bal_k3[len(bal_k3) - 2]
    #         stopky_b = pygame.time.get_ticks()
    #         PN_sub.zvuky(i, lezici)

    pygame.init()
    pygame.display.update()

# ukončení hry
    if [len(bal_a), len(leti_a), len(spec_a_1), len(spec_a_2)] == [0, 0, 0, 0]:
        hru_ukoncil_text = "Modrý hráč"
        hru_ukoncil_barva = MODRA
        prubeh_hry = "vyhodnocení"
    elif [len(bal_b), len(leti_b), len(spec_b_1), len(spec_b_2)] == [0, 0, 0, 0]:
        hru_ukoncil_text = "Červený hráč"
        hru_ukoncil_barva = CERVENA
        prubeh_hry = "vyhodnocení"


# info, kdo hru ukončil
while prubeh_hry == "vyhodnocení":
    bal_k1.append(nul_karta)
    bal_k2.append(nul_karta)
    bal_k3.append(nul_karta)

    konec_score = PN_sub.vyhodnoceni(bal_k1, bal_k2, bal_k3, specialove, pavouk_ciha_a, pavouk_ciha_b)

    # porovnávání score hráčů v jednotlivých balíčcích
    for i in range(0, 5, 2):
        if konec_score[i][2] > konec_score[i + 1][2]:
            body_a += 1
        elif konec_score[i][2] < konec_score[i + 1][2]:
            body_b += 1
        print(konec_score[i], konec_score[i + 1])

    prubeh_hry = "sláva"

while prubeh_hry == "sláva":

    # vyhodnocení
    if body_a > body_b:
        vitez = "modrý hráč!"
        vitez_barva = MODRA
    elif body_a < body_b:
        vitez = "červený hráč!"
        vitez_barva = CERVENA
    else:
        vitez = "nikdo. Je to remíza."
        vitez_barva = (55, 15, 55)

    font_bada = pygame.font.Font("Fonts/BadaBoomCE.otf", 50)
    font_stand = pygame.font.Font(None, 25)

    kos_1 = str(konec_score[0][2]) + " : " + str(konec_score[1][2])
    kos_2 = str(konec_score[2][2]) + " : " + str(konec_score[3][2])
    kos_3 = str(konec_score[4][2]) + " : " + str(konec_score[5][2])

    text_ukoncil = font_bada.render(("Hru ukončil: "+ hru_ukoncil_text), True, hru_ukoncil_barva)
    text_kos1 = font_bada.render(kos_1, True, MODRA if konec_score[0][2] > konec_score[1][2] else CERVENA)
    text_kos2 = font_bada.render(kos_2, True, MODRA if konec_score[2][2] > konec_score[3][2] else CERVENA)
    text_kos3 = font_bada.render(kos_3, True, MODRA if konec_score[4][2] > konec_score[5][2] else CERVENA)
    text_modry_body = font_bada.render(("Modrý hráč získal bodů: " + str(body_a)), True, MODRA)
    text_cerveny_body = font_bada.render(("Červený hráč získal bodů: " + str(body_b)), True, CERVENA)
    text_vyhral = font_bada.render(("Vyhrál ... "+ vitez), True, vitez_barva)
    text_konec = font_stand.render(("Stiskni mezerník pro ukončení hry."), True, "Black")
    parchment = pygame.transform.rotozoom(pygame.image.load("Pic_grafika/Parchment.jpg"), 0, 0.4)


    screen.blit(parchment, (150, 50))
    screen.blit(text_ukoncil, (300, 100))
    screen.blit(text_kos1, (350, 170))
    screen.blit(text_kos2, (500, 170))
    screen.blit(text_kos3, (650, 170))
    screen.blit(text_modry_body, (300, 250))
    screen.blit(text_cerveny_body, (300, 320))
    screen.blit(text_vyhral, (300, 430))
    screen.blit(text_konec, (650, 550))

    PN_sub.konec()

    prubeh_hry = "konec"

    pygame.event.pump()
    pygame.init()
    pygame.display.update()

while prubeh_hry == "konec":
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        pygame.quit()
        exit()
    pygame.event.pump()


