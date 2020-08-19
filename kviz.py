import bottle
import model

SKRIVNOST = 'to_je_kviz'

seznam_kvizov = model.SeznamKvizov('stanje.json')

# Prikaz zacetne strani
@bottle.get('/')
def index():
    return bottle.template('views/index.tpl')


# naredi nov kviz
def nov_kviz(dolzina):
    id = seznam_kvizov.nov_kviz(dolzina)
    bottle.response.set_cookie('id', 'id{}'.format(id), secret=SKRIVNOST, path='/')

    seznam_kvizov.kvizi[id].generiraj_vprasanja()
    seznam_kvizov.shrani_v_datoteko()
    bottle.redirect('/kviz')

@bottle.get('/kviz10')
def nov_kviz_10():
    nov_kviz(2)

@bottle.get('/kviz25')
def nov_kviz_25():
    nov_kviz(25)

@bottle.get('/kviz50')
def nov_kviz_50():
    nov_kviz(50)


@bottle.route('/kviz')
def pokazi_vprasanje():
    id = int(bottle.request.get_cookie('id', secret=SKRIVNOST).split('d')[1])
    izbrana_drzava = bottle.request.query.drzava
    
    vprasanje = seznam_kvizov.kvizi[id].trenutno_vprasanje()
    print(len(izbrana_drzava))

    if len(izbrana_drzava) == 0:
        return bottle.template('views/kviz.tpl', vprasanje=vprasanje, je_ze_odgovarjal=False)
    else:
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

@bottle.get('/img/<picture>')
def serve_pictures(picture):
    return bottle.static_file(picture, root='podatki/drzave_img')


bottle.run(reloader=True, debug=True)