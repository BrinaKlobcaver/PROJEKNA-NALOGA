import bottle
import model

kviz = None

# Prikaz zacetne strani
@bottle.get('/')
def index():
    return bottle.template('views/index.tpl')


# naredi nov kviz
def nov_kviz(dolzina):
    global kviz
    kviz = model.Kviz(dolzina)
    kviz.generiraj_vprasanja()
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
    izbrana_drzava = bottle.request.query.drzava
    
    vprasanje = kviz.trenutno_vprasanje()
    print(len(izbrana_drzava))

    if len(izbrana_drzava) == 0:
        return bottle.template('views/kviz.tpl', vprasanje=vprasanje, je_ze_odgovarjal=False)
    else:
        pravilno = kviz.je_odgovor_pravilen(izbrana_drzava)
        je_odgovor_pravilen = pravilno[0]

        pravilen_odgovor = ''
        if je_odgovor_pravilen == False:
            pravilen_odgovor = pravilno[1]
        return bottle.template('views/kviz.tpl', vprasanje=vprasanje, je_ze_odgovarjal=True, je_odgovor_pravilen=je_odgovor_pravilen, pravilen_odgovor=pravilen_odgovor)


@bottle.get('/naslednje_vprasanje')
def naslednje_vprasanje():
    kviz.naslednje_vprasanje()
    if kviz.ze_vse_odgovorjeno():
        bottle.redirect('/rezultati')
    else:
        bottle.redirect('/kviz')

@bottle.get('/rezultati')
def rezultati():
    return bottle.template('views/rezultati.tpl', odstotek_pravilnih=kviz.odstotek_pravilnih())

@bottle.get('/img/<picture>')
def serve_pictures(picture):
    return bottle.static_file(picture, root='podatki/drzave_img')


bottle.run(reloader=True, debug=True)