<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Resultado do Jogo do EICA</title>
    <link rel="stylesheet" href="/static/tablestyle.css" type="text/css" />
</head>
<body>
    <h1>Resultado do Jogo Cartas Voadoras</h1>
    <h2>Usuário: {{user}}</h2>
    <table id="box-table-a" >

        <thead>
            <tr>
                <th scope="col"><span>Carta</span></th>

                <th scope="col"><span>Casa</span></th>

                <th scope="col"><span>Movimento</span></th>

                <th scope="col"><span>Pontos</span></th>

                <th scope="col"><span>Tempo</span></th>

                <th scope="col"><span>Resultado</span></th>

            </tr>
        </thead>


        <tbody>
            % for line in result:
            <tr>
                <td><span>{{ line["carta"] }}<span></td>
                <td><span>{{ line["casa"] }}<span></td>
                <td><span>{{ line["move"] }}<span></td>
                <td><span>{{ line["ponto"] }}<span></td>
                <td><span>{{ line["tempo"] }}<span></td>
                <td><span>{{ line["valor"] }}<span></td>
            </tr>
            % end
        </tbody>

    </table>
</body>
</html>
