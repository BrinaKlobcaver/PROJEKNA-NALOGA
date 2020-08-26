import bottle
import model

SKRIVNOST = 'to_je_kviz'

seznam_kvizov = model.SeznamKvizov('stanje.json')

# Prikaz zacetne strani
@bottle.get('/')
def index():
    return bottle.template('views/index.tpl')


# naredi nov kviz
@bottle.get('/kviz/<dolzina>')#število vprašanj(tri funkcije v eni)
def nov_kviz(dolzina):
    id = seznam_kvizov.nov_kviz(int(dolzina))
    bottle.response.set_cookie('id', 'id{}'.format(id), secret=SKRIVNOST, path='/')

    seznam_kvizov.kvizi[id].generiraj_vprasanja()
    seznam_kvizov.shrani_v_datoteko()
    bottle.redirect('/kviz')



@bottle.route('/kviz')
def pokazi_vprasanje():
    id = int(bottle.request.get_cookie('id', secret=SKRIVNOST).split('d')[1])
    izbrana_drzava = bottle.request.query.drzava
    
    vprasanje = seznam_kvizov.kvizi[id].trenutno_vprasanje()

    if len(izbrana_drzava) == 0:# če še nobena država ni bila izbrana
        return bottle.template('views/kviz.tpl', vprasanje=vprasanje, je_ze_odgovarjal=False)
    else:#če pa je odgovoril
        pravilno = seznam_kvizov.kvizi[id].je_odgovor_pravilen(izbrana_drzava)
        seznam_kvizov.shrani_v_datoteko()

        je_odgovor_pravilen = pravilno[0]

        pravilen_odgovor = ''
        if je_odgovor_pravilen == False:
            pravilen_odgovor = pravilno[1]
        return bottle.template('views/kviz.tpl', vprasanje=vprasanje, je_ze_odgovarjal=True, je_odgovor_pravilen=je_odgovor_pravilen, pravilen_odgovor=pravilen_odgovor)


@bottle.get('/naslednje_vprasanje')
def naslednje_vprasanje():
    id = int(bottle.request.get_cookie('id', secret=SKRIVNOST).split('d')[1])

    seznam_kvizov.kvizi[id].naslednje_vprasanje()
    seznam_kvizov.shrani_v_datoteko()
    if seznam_kvizov.kvizi[id].ze_vse_odgovorjeno():
        bottle.redirect('/rezultati')
    else:
        bottle.redirect('/kviz')

@bottle.get('/rezultati')
def rezultati():
    id = int(bottle.request.get_cookie('id', secret=SKRIVNOST).split('d')[1])
    return bottle.template('views/rezultati.tpl', odstotek_pravilnih=seznam_kvizov.kvizi[id].odstotek_pravilnih())

@bottle.get('/zacni-ponovno')#briše kviz iz spomina(ko klikneš zacni ponovno)
def zacni_ponovno():
    id = int(bottle.request.get_cookie('id', secret=SKRIVNOST).split('d')[1])
    seznam_kvizov.kvizi.pop(id)
    seznam_kvizov.shrani_v_datoteko()

    bottle.redirect('/')#preusmeri na začetno stran


@bottle.get('/img/<picture>')
def serve_pictures(picture):
    return bottle.static_file(picture, root='podatki/drzave_img')


bottle.run(reloader=True, debug=True)#zažene server in izpiše naslov(http)