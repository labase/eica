<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Jogo EICA</title>
        <meta http-equiv="content-type" content="application/xml;charset=utf-8" />
        <link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
        <style>
            canvas {   display : block;   margin : auto;}
            body { background: #7ec0ee; }
        </style>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/phaser/2.6.1/phaser.min.js"></script>
        <script type="text/javascript" src="https://cdn.rawgit.com/brython-dev/brython/3.2.6/www/src/brython.js"></script>
        <script type="text/python">
            from eica.main import main
            from braser import Braser
            main("{{ doc_id }}")
        </script>
    </head>
    <body onLoad="brython(1, {static_stdlib_import: true})" class="main">
        <div id="pydiv">
                <span style="color:white">AGUARDE..</span>
                <img src="/static/assets/raincloud.gif" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);" alt="carregando"></img>

        </div>


    <script src='http://codepen.io/assets/libs/fullpage/jquery.js'></script>
    </body>
</html>