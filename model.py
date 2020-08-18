import random

class Vprasanje():
    def __init__(self, drzava, indeks_drzave, seznam_drzav):
        self.pravilni_odgovor = drzava
        self.indeks_drzave = indeks_drzave

        drzave_brez_pravilne = []
        for d in seznam_drzav:
            if not d == drzava:
                drzave_brez_pravilne.append(d) #doda (nepravilno) državo v seznam (na konec)
        random.shuffle(drzave_brez_pravilne) # premesa seznam

        odgovori = [drzava]
        odgovori.extend(drzave_brez_pravilne[0:3]) # tri nakljucne drzave
        random.shuffle(odgovori) # premesa odgovore

        self.odgovori = odgovori




class Kviz():
    def __init__(self, st_vprasanj):
        # Prebere imena drzav iz datoteke
        with open('podatki/imena_drzav.txt', 'r', encoding='utf-8') as file:
            seznam = file.readlines()
        for i in range(len(seznam)):
            seznam[i] = seznam[i][:-1]
        self.seznam_drzav = seznam

        self.indeks_trenutnega_vprasanja = 0
        self.st_pravilnih_odgovorov = 0
        self.st_vprasanj = st_vprasanj
    
    def generiraj_vprasanja(self):
        seznam_vprasanj = []
        for i in range(len(self.seznam_drzav)):
            drzava = self.seznam_drzav[i]
            v = Vprasanje(drzava, i, self.seznam_drzav) # vprasanje za vsako drzavo
            seznam_vprasanj.append(v)

        random.shuffle(seznam_vprasanj) #da je vedno drug vrstni red držav pri vprašanjih

        self.seznam_vprasanj = seznam_vprasanj
    

    def trenutno_vprasanje(self):
        return self.seznam_vprasanj[self.indeks_trenutnega_vprasanja] #da šteje
    
    def je_odgovor_pravilen(self, odgovor):
        if odgovor == self.trenutno_vprasanje().pravilni_odgovor:
            self.st_pravilnih_odgovorov += 1
            return [True]
        else:
            self.st_pravilnih_odgovorov += 0
            return [False, self.trenutno_vprasanje().pravilni_odgovor]
    
    def naslednje_vprasanje(self):
        self.indeks_trenutnega_vprasanja += 1
    
    def odstotek_pravilnih(self):
        return self.st_pravilnih_odgovorov / self.st_vprasanj





# Testiranje: 
kviz = Kviz()
kviz.generiraj_vprasanja()

'''
for i in range(5):
    vprasanje = kviz.trenutno_vprasanje()
    for odgovor in vprasanje.odgovori:
        print(odgovor)
    odgovor = input()

    x = kviz.je_odgovor_pravilen(odgovor)
    if x[0] == True:
        print('Pravilno')
    else:
        print('Narobe, ', x[1])
    
    input()
    kviz.naslednje_vprasanje()
'''