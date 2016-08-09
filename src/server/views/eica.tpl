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
            from browser import doc
            ver = main("{{ doc_id }}")
            doc["versiontext"].text = ver
        </script>
    </head>
    <body onLoad="brython(1, {static_stdlib_import: true})" class="main">
        <div style="position:relative; min-height:100%;">
            <div id="pydiv">
                <span style="color:white">AGUARDE..</span>
                <img src="assets/caveman.gif" style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);" alt="carregando"></img>
            </div>
            <div id="version" style="position:fixed; bottom:0px;">
                <span id="versiontext" style="color:white;"></span>
            </div>
        </div>
        <script src='http://codepen.io/assets/libs/fullpage/jquery.js'></script>
    </body>
</html>