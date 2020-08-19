<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">

    <style>
        .btn {
            margin-bottom: 5px;
        }

        #seznam-vprasanj {
            margin-top: 2em;
        }
        #seznam-vprasanj .btn {
            margin-top: 0.8em;
        }

        #seznam-vprasanj .text-left {
            margin-left: auto;
            margin-right: auto;
            width: fit-content;
        }

        
        body {
            margin-top: 1em;
        }
    </style>

    <title>Kviz</title>
</head>
<body>
    <div class="container text-center">
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

    </div>
    
</body>
</html>