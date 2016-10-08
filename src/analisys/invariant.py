from bottle import template
import itertools
WNC = '''Tabela gerada por rede neural sem peso para derivada segunda do tempo com prognósticos'''
WNN = '''                  renan   felipe da vila V V:  134849 F:   37229 S:   22271 E:  -87321  conf: 72
                        ANTONIOGUILHERME F F:   80263 S:  -30609 V:  -70742 E: -113902  conf: 100
                 Ana Fernanda Dos Santos S S:   98866 V:   96966 F:   67414 E:  -78573  conf: 1
           Cassiana da silva de maria None F:  -89869 S: -113888 E: -145025 V: -253250  conf: 26
                Christian Rodrigues Gago F F:   95669 S:  -44375 E: -119712 V: -125172  conf: 100
 Ester Helen Rodrigues Cordeiro De Brito E E:   47930 F:  -93252 S: -191065 V: -428494  conf: 100
       Evellyn Vitoria Feitosa Araujo None V:  152050 F:   44927 S:   22676 E:  -73656  conf: 70
                   JORGE   FILIPPE    None F:  -32248 S:  -69527 E: -120554 V: -143252  conf: 100
       Jade Feitosa Matias Dos Santos None F:    -463 S:  -29565 V:  -43178 E: -109543  conf: 100
      Julia Gabrielly Nascimento Marques E E:   -6201 F:  -85413 S: -115841 V: -264485  conf: 100
                     Kamille De Oliveira V V:   -3223 F:  -43604 S:  -64529 E: -129700  conf: 100
                              LARISSA None F:   -7623 S:  -52858 V:  -88350 E: -114493  conf: 100
               Laiza Fernandes De Farias V V:  122223 F:   15321 S:  -10024 E: -103704  conf: 87
             Maria Eduarda Da Silva Lima E E:   -1851 F:  -11227 S:  -57346 V:  -93280  conf: 100
      Pitter Guimaraes Correia Goncalves V V:  174993 F:   39361 S:   11806 E:  -77233  conf: 77
                            Samuel Gomes V V:    3416 F:   -7130 S:  -44851 E:  -95215  conf: 100
             Tatiane Monteiro Nascimento V F:   48688 E:   20199 S:  -70844 V:  -79745  conf: -58
            Tatiane Monteiro Nascimento1 V E:  -84869 F: -126169 S: -225846 V: -369933  conf: -48
                      Thiago Gens Pasche V V:  195569 F:   60379 S:   24647 E:  -70138  conf: 69
                             anderson None V:  173212 F:   60785 S:   41628 E:  -65754  conf: 64
    arthu  willian tavares dos santos None E: -179748 F: -196993 S: -290499 V: -654430  conf: 9
                             carolina None V:   88993 F:   22976 S:   -9883 E:  -86767  conf: 74
                  filipe balbino ribeiro F F:  112512 V:   52117 S:   -4327 E:  -76128  conf: 53
         jhonathan  bordoni teixeira  None V:   65174 F:   33412 S:    4973 E:  -83845  conf: 48
            julie brenda santos da silva V V:  164661 F:   28145 S:    9430 E:  -91985  conf: 82
                                    kaue V V:  150755 F:   20427 S:    2596 E:  -88432  conf: 86
                 kayke juan silva bastos F F:   54874 E:   32462 S:  -17315 V:  -22905  conf: 40
               keyla cardoso de carvalho E E:   20263 F: -133310 S: -234582 V: -542169  conf: 100
         linda iasmin de olivera macede  V V:   22044 F:  -17895 S:  -54511 E:  -99571  conf: 100
                    maria eduarda alves  E E:   62069 F:   31585 S:  -39752 V:  -69920  conf: 49
          patrick de oliveira nascimento S S:   68407 F:    6678 V:  -27418 E: -110579  conf: 90
         patrick de oliveira nascimento1 S S:   79115 V:   40308 F:   21364 E:  -79760  conf: 49
                   radames felipe davila F F:  -96962 E: -239740 S: -336897 V: -824298  conf: 100
    rafaelly santiago da silva fortes None F:   -4422 V:   -9788 S:  -33966 E: -109082  conf: 100
          toni carlos souza dos prazeres F F:   80908 E:   23247 S:  -70227 V: -109184  conf: 71
       wesleyana vitoria aquino de souza V V:  190069 F:   47586 S:   27987 E:  -72765  conf: 74
'''.split("\n")

WNNTABLE = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <style type="text/css">

          table.t1 {
            margin: 1em auto;
            border-collapse: collapse;
            font-family: Arial, Helvetica, sans-serif;
          }
          .t1 th, .t1 td {
            padding: 4px 8px;
          }
          .t1 thead th {
            background: #4f81bd;
            text-transform: lowercase;
            text-align: left;
            font-size: 15px;
            color: #fff;
          }
          .t1 tr {
            border-right: 1px solid #95b3d7;
          }
          .t1 tbody tr {
            border-bottom: 1px solid #95b3d7;
          }
          .t1 tbody tr:nth-child(odd) {
            background: #dbe5f0;
          }
          .t1 tbody th, .t1 tbody tr:nth-child(even) td {
            border-right: 1px solid #95b3d7;
          }
          .t1 tfoot th {
            background: #4f81bd;
            text-align: left;
            font-weight: normal;
            font-size: 10px;
            color: #fff;
          }
          .t1 tr *:nth-child(3), .t1 tr *:nth-child(4) {
            text-align: right;
          }

        </style>
    </head>
    <body>
        <table class="t1" summary="{{summary}}">
        <caption>{{caption}}</caption>
        <thead>
        % for head in header:
            <th>{{head}}</th>
        %end
        </thead>
        <tbody>
        % for line in table:
            <tr><th>{{line["head"]}}</th>
            % for data in line["data"]:
                <td>{{data}}</td>
            % end
            </tr>
        %end
        </tbody>
        <tfoot>
        <tr><th colspan="{{cols}}">{{foot}}</th></tr>
        </tfoot>
        </table>
    </body>
</html>
"""
HEAD = "Nome do aluno,PG,C 0,Nota 0,C 1,Nota 1,C 2,Nota 2,C 3,Nota 3,Conf.".split(",")
FOOT = "PG: Prognóstico; Confiança Total: 69"


def wnnhtmltable(data=WNN, head=HEAD, foot=FOOT, filename="stats_table.html", formater=WNNTABLE):
    data = [[cell.split() if icell != 0 else [" ".join(cell.split()[:-2])]+[cell.split()[-2]]+[cell.split()[-1]]
             for icell, cell in enumerate(line.split(":"))]
            for line in data[:-1]]
    # print(data)
    data = [itertools.chain(*line) for line in data]
    data = [dict(head=head, data=line+[conf]) for head, *line, _, conf in data]
    # print(data)
    templater = template(formater, caption=WNC, summary=WNC, foot=foot, header=head, table=data, cols=len(head))
    print(templater)
    with open(filename, 'w') as hfile:
        hfile.write(templater)


def htmltable(data=WNN, head=HEAD, foot=FOOT, filename="stats_table.html", caption=WNC, formater=WNNTABLE):
    data = [dict(head=head, data=line) for head, *line in data]
    # print(data)
    summary = caption
    templater = template(formater, caption=caption, summary=caption, foot=foot, header=head, table=data, cols=len(head))
    # print(templater)
    with open(filename, 'w') as hfile:
        hfile.write(templater)


if __name__ == '__main__':
    wnnhtmltable()
