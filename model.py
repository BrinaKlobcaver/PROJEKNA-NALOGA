import random
import json

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
        self.st_vprasanj = st_vprasanj

        self.pravilnost_odgovorov = [False for i in range(50)]
    
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
            self.pravilnost_odgovorov[self.indeks_trenutnega_vprasanja] = True
            return [True]
        else:
            self.pravilnost_odgovorov[self.indeks_trenutnega_vprasanja] = False
            return [False, self.trenutno_vprasanje().pravilni_odgovor]
    
    def naslednje_vprasanje(self):
        self.indeks_trenutnega_vprasanja += 1
    
    def odstotek_pravilnih(self):
        st_pravilnih_odgovorov = 0
        for je_pravilen in self.pravilnost_odgovorov:
            if je_pravilen:
                st_pravilnih_odgovorov += 1
        
        return st_pravilnih_odgovorov / self.st_vprasanj
    
    def ze_vse_odgovorjeno(self):
        return self.indeks_trenutnega_vprasanja >= self.st_vprasanj



class SeznamKvizov():
    def __init__(self, datoteka_s_stanjem):
        self.kvizi = {}
        self.id_naslednjega_kviza = 0
        self.datoteka_s_stanjem = datoteka_s_stanjem
    
    def nov_kviz(self, dolzina):
        nov = Kviz(dolzina)
        self.kvizi[self.id_naslednjega_kviza] = nov
        trenutni_id = self.id_naslednjega_kviza
        self.id_naslednjega_kviza += 1

        return trenutni_id

    def pretvori_kviz_v_slovar(self, kviz):
        seznam_vprasanj = []
        for vprasanje in kviz.seznam_vprasanj:
            slovar = {
                'drzava': vprasanje.pravilni_odgovor,
                'odgovori': vprasanje.odgovori,
                'indeks_drzave': vprasanje.indeks_drzave
            }
            seznam_vprasanj.append(slovar)

        slovar = {
            'st_vprasanj': kviz.st_vprasanj,
            'indeks_trenutnega_vprasanja': kviz.indeks_trenutnega_vprasanja,
            'pravilnost_odgovorov': kviz.pravilnost_odgovorov,
            'seznam_drzav': kviz.seznam_drzav,
            'seznam_vprasanj': seznam_vprasanj
        }
        return slovar

    def shrani_v_datoteko(self):
        slovar_kvizov = {}
        for (id, kviz) in self.kvizi.items():
            slovar_kvizov[id] = self.pretvori_kviz_v_slovar(kviz)


        slovar = {
            'datoteka_s_stanjem': self.datoteka_s_stanjem,
            'id_naslednjega_kviza': self.id_naslednjega_kviza,
            'kvizi': slovar_kvizov
        }

        with open(self.datoteka_s_stanjem, 'w', encoding='utf-8') as f:
            json.dump(slovar, f)