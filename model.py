import random
import json
import os.path


class Vprasanje():
    def __init__(self, drzava, indeks_drzave, seznam_drzav):
        self.pravilni_odgovor = drzava
        self.indeks_drzave = indeks_drzave

        drzave_brez_pravilne = []
        for d in seznam_drzav:
            if not d == drzava:
                # doda (nepravilno) državo v seznam (na konec)
                drzave_brez_pravilne.append(d)
        random.shuffle(drzave_brez_pravilne)  # premesa seznam

        odgovori = [drzava]
        odgovori.extend(drzave_brez_pravilne[0:3])  # tri nakljucne drzave
        random.shuffle(odgovori)  # premesa odgovore

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
            # vprasanje za vsako drzavo
            v = Vprasanje(drzava, i, self.seznam_drzav)
            seznam_vprasanj.append(v)

        # da je vedno drug vrstni red držav pri vprašanjih
        random.shuffle(seznam_vprasanj)

        self.seznam_vprasanj = seznam_vprasanj

    def trenutno_vprasanje(self):
        # da šteje
        return self.seznam_vprasanj[self.indeks_trenutnega_vprasanja]

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


class SeznamKvizov():  # za več uporabnikov
    def __init__(self, datoteka_s_stanjem):
        self.kvizi = {}
        self.id_naslednjega_kviza = 0
        self.datoteka_s_stanjem = datoteka_s_stanjem

        if os.path.exists(datoteka_s_stanjem):  # za branje datoteke, če ta obstaja
            self.preberi_iz_datoteke()

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

    def preberi_iz_datoteke(self):  # da lahko nadaljuješ kviz od tam, kjer si ostal
        with open(self.datoteka_s_stanjem, 'r', encoding='utf-8') as f:
            slovar = json.load(f)

        self.datoteka_s_stanjem = slovar['datoteka_s_stanjem']
        self.id_naslednjega_kviza = int(slovar['id_naslednjega_kviza'])
        self.kvizi = {}
        for (id, kviz_slovar) in slovar['kvizi'].items():
            self.kvizi[int(id)] = self.pretvori_slovar_v_kviz(kviz_slovar)

    def pretvori_slovar_v_kviz(self, kviz_slovar):
        kviz = Kviz(int(kviz_slovar['st_vprasanj']))
        kviz.st_vprasanj = int(kviz_slovar['st_vprasanj'])
        kviz.indeks_trenutnega_vprasanja = int(
            kviz_slovar['indeks_trenutnega_vprasanja'])
        kviz.pravilnost_odgovorov = kviz_slovar['pravilnost_odgovorov']
        kviz.seznam_drzav = kviz_slovar['seznam_drzav']

        kviz.seznam_vprasanj = []
        for vprasanje_slovar in kviz_slovar['seznam_vprasanj']:
            vprasanje = Vprasanje(
                vprasanje_slovar['drzava'], vprasanje_slovar['indeks_drzave'], kviz_slovar['seznam_drzav'])
            vprasanje.pravilni_odgovor = vprasanje_slovar['drzava']
            vprasanje.odgovori = vprasanje_slovar['odgovori']
            vprasanje.indeks_drzave = int(vprasanje_slovar['indeks_drzave'])
            kviz.seznam_vprasanj.append(vprasanje)

        return kviz
