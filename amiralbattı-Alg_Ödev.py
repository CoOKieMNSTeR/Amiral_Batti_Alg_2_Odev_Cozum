#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import random
from time import sleep
from copy import deepcopy

gemiler = {
    'Savasgemisi': {'boyut': 4, 'isaret': 'S'},
    'Denizalti': {'boyut': 3, 'isaret': 'D'},
    'Yokedici': {'boyut': 2, 'isaret': 'Y'},
    'Tasiyici': {'boyut': 1, 'isaret': 'T'},
}
# Gemileri isim istenen boyut ve tahta(grid) üzerinde harf gösterimi olarak tanımladık.

def ayarla_yer(gemi): #Bütün tahta için gemi yerleştirme işlemi yapan fonksyon.
    yuvalar = [] # İstenen şekilde liste

    for sat in range(boy):
        for kol in range(en - gemi['boyut'] + 1): # O anki geminin boyutu kadar satırda yerleştir.
            slot = []
            for i in range(gemi['boyut']):
                if grid[sat][kol+i] == '?': # Gemiler satırda üst üste gelmemesi için kontrol.
                    slot.append([sat, kol+i])  #Yerleştir.
                else:
                    slot = []
                    break
            else:
                yuvalar.append(slot) #Gemilerin yerini listeye ekle

    for kol in range(en):
        for sat in range(boy - gemi['boyut'] + 1): #O anki geminin boyutu kadar sutunda yerleştir.
            for i in range(gemi['boyut']):
                if grid[sat+i][kol] == '?': #Gemiler sutunda üst üste gelemsin diye kontrol.
                    slot.append([sat+i, kol]) # Yerleştir
                else: #Atla
                    slot = []
                    break
            else:
                yuvalar.append(slot) #Gemilerin yerini listeye ekle
            slot = []

    return yuvalar #Gemilerin yerini döndür.


def gemileri_yerlestir():
    for gemi in gemiler.values(): #Gemilerin sayısı kadar dön
        yuvalar = ayarla_yer(gemi) #gemiler için boyutu kadar yer ayır.
        rast_yuva = random.choice(yuvalar) # rastgele bir şekilde en boy içinde bir yer değişkeni al.
        isaret_yer(rast_yuva, gemi) #Rastgele alınan yerden başlayarak yatay veya dikey yerleştirmek için fonksyona gönder.


def isaret_yer(slot, gemi):
    for x, y in slot: #belirlenen yere geminin işaretlerini koy.
        grid[x][y] = gemi['isaret']


def tahta_goster(grid):
    os.system('cls') # Ekranı temizle
    for sat in grid:
        print (' '.join(sat)) #gönderilen grid deki tahtayı göster.
    print()


def tahmin_al():
    while True:
        tahminci = input('\nTahmin x y\n----> ') # Kullanıcıdan tahmin al
        if tahminci in ['goster', 'hile']: #Eğer goster veya hile yazarsa direk 
            return tahminci #hile veya gosteri dön
        try: #Hile veya goster yazmazsa 
            x, y = map(int, tahminci.split()) # gönderilen iki koordinat değerini split ile ayırarak x ve y değişkenine ata.
            if x not in range(en) or y not in range(boy): # x ve y nin tahtanın belirtilen en ve boy değeri içinde mi olduğuna bak.
                print ('\nHata : Okyanusun Disina Ciktin........') # Değilse kullanıcıyı uyar.
                print ('0 ile 9 arasi değerler gir.\n'.format(en, boy)) # Ve hangi değerler arasında girmesi gerektiğini belirt
                continue
            return x + 1, y + 1
        except Exception:
            print ('\nKoordinatları şu formatta boşluklu gir: x y \neg--> 0 0\neg--> 3 7') # Eğer istenen şekilde boşluk bırakılarak girilmezse
            #örnek göstererek kullanıcıyı uyar.


def tahminci_vur():
    global kul_eski
    while True:
        tahminci = tahmin_al() # Kullanıcıdan tahmin al.

        if tahminci in ['goster', 'hile']: # Oyuncu hile veya goster yazarsa 
            tahta_goster(grid) #Arka plandaki asıl tahtayı göster.
        else: #Yazmazsa tahmin işlemine geç.
            if tahminci in kul_eski: # Eğer eskiden girmiş olduğu bir koordinatsa 
                print ('\nSen aynı yeri tahmin etmistin. Tekrar dene.\n') # Bunu kullancıya belirt.
                continue
            tahmin_x, tahmin_y = tahminci
            kul_eski.append(tahminci)
            break
    alan_ic = grid[tahmin_y][tahmin_x]
    if alan_ic != '?': # arka planda bir gemiye karşılık gelen örneğin "D" var ise gemi vuracağımız için buraya gir
        grid[tahmin_y][tahmin_x] = 'X' #Tahtada ve oyuncu_tahtasında istenen şeklide 'X' ile doldurduk
        oyuncu_grid[tahmin_y][tahmin_x] = 'X'
        rem = 0
        for sat in grid:
            if alan_ic in sat: #Geminin tamamı vurulmadıysa gir
                rem += 1
        if rem == 0:
            for type, gemi in gemiler.items():
                if alan_ic == gemi['isaret']: # Tamamı vurulan geminin isaretine göre ekrana o gemiyi basıcağız 
                    print ('\n...')
                    sleep(.75)
                    print ('...')
                    sleep(.75)
                    print ('... Tebrikler siz benim şu gemimi batırdınız ==> {} !!!\n'.format(type)) 
                    sleep(3)
            tahta_goster(oyuncu_grid) # oyuncuya tahtasını göster.
            return True
        else: #gemininin tamamı vurulmadıysa.
            print ('\n...Tebrikler Bir Gemi Vurdunuz ...\n') # Vurduğunu kullanıcıya belirttik.
            sleep(1)
            tahta_goster(oyuncu_grid)
    else:
        grid[tahmin_y][tahmin_x] = '*' #Tahtada ve oyuncu tahtasında tahmin edilen yeri istenen şekilde karavanaya karşılık gelen * karakteri
        oyuncu_grid[tahmin_y][tahmin_x] = '*' # ile doldurduk.
        print ('\n... Maalesef İsabet Ettiremediniz ...\n') # Vuramadığını kullanıcıya söyledik.
        sleep(1)
        tahta_goster(oyuncu_grid) #Oyuncuya tahtasını göster.


def kazan_bas(hak):
    if hak != 33: #Hak sayısından değilde bütün gemiler vurulduğu için ise
        for i in range(3): # 3 Kez basıyoruz biraz atari salonları gibi olsun istedim :)
            print ('!!! Şu kadar puan kazandın !!!')
            print ('=====>',(33-hak),"<=====" ) #İstenen şekilde puanı hesapla ve ekrana bas
            sleep(2)
            tahta_goster(grid_kopya)
            print (hak,'Hak Kullanarak')
            print ('Bütün Gemiler Battırdın !!!') #Kaç hak kullanarak kazandığını yazdık.
            sleep(2)
            tahta_goster(oyuncu_grid)
    else:
        print("Basarisiz Oldun Hakkini Bitirdin!!!") #33 hakkını kullanarak geldi ise oyunu kaybettiğini belirttik.
        sleep(2)
   

if __name__ == '__main__':
    while 1:
        os.system('cls') # Ekranı temizledik.
        print ('\n **** Amiral Batti Oyununa Hosgeldin **** \n')
        sleep(1) # 1 saniye bekletme
        print ('Sadece koordinat gir (hile veya goster yazma )')
        sleep(1)
        print ('Ben sana vurursan soylerim. \n')
        sleep(1)
        en = 10 # İstenen en ve boy değerlerini girdik.
        boy = 10
        print ('Tanimli boyut {}x{}.'.format(en, boy)) # en boyu ekranda gösterdik
        print()
        grid = [] # tahtayı ve oyuncu için tahtayı oluşturduk (İstendiği gibi liste)
        oyuncu_grid = []
        grid.append([' '] + list(map(str, range(en)))) # tahtamızı ve oyuncu tahtamızı en , boy oranına göre oluşturduk.
        oyuncu_grid.append([' '] + list(map(str, range(en))))
        for i in range(boy):
            grid.append([str(i)] + ['?'] * en) # tahtamızı ve oyuncu tahtamızı en , boy oranına göre istenen ? karakteri ile doldurduk.
            oyuncu_grid.append([str(i)] + ['?'] * en)
        tahta_goster(oyuncu_grid) # oyuncuya tahtasını gösterdik.
        gemileri_yerlestir() # Tahtaya gemileri yerleştirme fonksyonu
        grid_kopya = deepcopy(grid) #tahtanın bir kopyasını aldık.
        gemi_kalan = len(gemiler) # Toplam gemi sayısını gemi_kalan değişkenine atadık.
        hak = 0 # Maksimum hak hesaplaması için kullanıcağımız değişkeni oluşturduk.
        kul_eski = [] #oyuncunun gireceği koordinatlar tutulmalı
        while gemi_kalan > 0 and hak != 33: # gemi saysısı 0 dan büyük ve hak sayısı hesaplanan 33 den farklı ise oyuncu tahmin yapmalı
            print ('{} gemi kaldı'.format(gemi_kalan)) # Kalan gemi sayısını ekrana yazdık.
            if tahminci_vur(): #Eğer tahmin edilip geminin tamamı vurulursa gemi sayısını 1 azalt
                gemi_kalan -= 1
            hak += 1 #Her tahminde hak saysısını 1 arttır ve kullanıcıya bunu belirt.
            print(hak,'.Hakkını kullandın')
        else:
            kazan_bas(hak) #Tahmin sayısı 33 olmuş veya bütün gemiler vurulumuş ise kazanma veya kaybetme durumunu basmak için kazan_bas fonskyonuna git

        devammi = input('\n"tamam" mı "devam" mı?\n----> ') #Kullanıcıya tekrar oynamak istiyor mu sor.

        if devammi == "tamam": # Eğer oynamak istemiyorsa while sonsuz döngüsünü kır ve programı kapat.
            break

