% rebase('base.tpl', title='Kviz')


<h2 class="lead" >Katera zvezna država je to? </h2>
<img src="/img/{{vprasanje.indeks_drzave}}.jpg" />

% if je_ze_odgovarjal:
    <div>
        <br />
        <h2 class="lead">
        % if je_odgovor_pravilen:
            Pravilno!
        % else:
            Narobe. Pravilen odgovor je {{pravilen_odgovor}}
        % end
        </h2>
        <a href="./naslednje_vprasanje" class="btn btn-outline-primary">Naprej</a>
    </div>

% else:
    <form id="seznam-vprasanj">
        <div class="text-left">
        % for drzava in vprasanje.odgovori:
            <input type="radio" value="{{drzava}}" id="{{drzava}}" name="drzava">
            <label for="{{drzava}}">{{drzava}}</label> <br />
        % end
        </div>

        <input class="btn btn-primary" type="submit" value="OK">
    </form>
% end