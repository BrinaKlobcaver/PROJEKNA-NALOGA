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

        .display-4 {
            font-size: 2em;
        }

        .lead strong {
            color: #c00;
        }

        body {
            margin-top: 1em;
        }
    </style>

    <title>Kviz</title>
</head>
<body>
    <div class="container text-center">
        <h1 class="display-4">Juhuuuuu, prišel si do konca kviza!</h1>
        <p class="lead" >Tvoj rezultat je: <strong>{{odstotek_pravilnih * 100}}%</strong></p>
    
        <a href="./" class="btn btn-primary">Začni ponovno</a>
    
    </div>
    
</body>
</html>