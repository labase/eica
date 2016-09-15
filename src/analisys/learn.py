# -*- coding: UTF8 -*-
from tinydb import TinyDB, Query
import os
from csv import writer
# import operator
# from datetime import datetime as dt
# from datetime import timedelta as td
# from time import strftime
# import matplotlib.pyplot as plt

Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S"
JSONDB = os.path.dirname(__file__) + '/eica_new.json'
KEYS = {'ano': 3, 'user': 40, 'hora': 20,
        'trans': 8, 'sexo': 12, 'prog': 1, 'nota': 1, 'idade': 2}
KEYLIST = 'user ano idade sexo trans prog nota hora'.split()
FORMAT = " ".join("{key}: {{{key}: <{val}}}".format(key=key, val=KEYS[key]) for key in KEYLIST)
TURN = {'tempo': 12, 'valor': 10, 'casa': 7, 'ponto': 8, 'carta': 12, 'delta': 12}
TURNLIST = 'tempo delta valor casa ponto carta'.split()
TURNFORMAT = " ".join("{key}: {{{key}: <{val}}} ".format(key=key, val=TURN[key]) for key in TURNLIST)


class Learn:
    def __init__(self, path=JSONDB):
        self.banco = TinyDB(path)
        self.query = Query()

    def report_user_data(self):
        values = self.banco.all()
        print(len(values))
        dem = ["user", "idade", "sexo", "ano", "hora"]
        print(FORMAT)
        # print(FORMAT.format(**{key: val for key, val in values[3].items() if key != "jogada"}))
        print({key: val or "#" for key, val in values[3].items() if key != "jogada"})
        for i, name in enumerate(values):
            format_string = "{:3d} "+FORMAT
            data = {key: val or "#" for key, val in name.items() if key != "jogada"}
            print(format_string.format(i, **data))

    def report_user_turn(self, u_name="LARISSA"):
        user = self.banco.search(self.query.user == u_name)[0]
        print(len(user["jogada"][0]))
        dem = ["user", "idade", "sexo", "ano", "hora"]
        print(user["jogada"][0])
        print(TURNFORMAT.format(**{key: val for key, val in user["jogada"][0].items()}))
        # return
        # print({key: val or "#" for key, val in values[3].items() if key != "jogada"})
        for i, name in enumerate(user["jogada"]):
            format_string = "{:3d} "+TURNFORMAT
            data = {key: val or "#" for key, val in name.items()}
            print(format_string.format(i, **data))

    def build_User_table_for_prog(self, measure="delta", prog="prog", slicer=32, filename="/table.tab", learn=0):
        """
        Gera um arquivo csv compatível com o Orange

        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param prog: Um dos possíveis prognosticos do banco: prog, nota, trans, sexo, idade, ano
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :param learn: 0 - inclui todos; 1 - só os que tem calsse; -1 - só os que não tem classe
        :return:
        """
        def sigla(name):
            return ' '.join(n.capitalize() if i == 0 else n.capitalize()[0]+"." for i, n in enumerate(name.split())) + name[-1]
        data = [
            [sigla(user["user"]), user[prog]] +
            [float(turn[measure])-float(turn0[measure]) for turn, turn0 in zip(user["jogada"][1:slicer], user["jogada"][:slicer])] for user in self.banco.all()]
        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            w = writer(writecsv, delimiter='\t')
            w.writerow(['n', 'CL'] + ['t%d' % t for t, _ in enumerate(data[1][:-1])])  # primeiro cabeçalho
            w.writerow(['d']+['d' if t == 0 else 'c' for t, _ in enumerate(data[1])])
            w.writerow(['m']+['c' if t == 0 else '' for t, _ in enumerate(data[1])])
            for line in data:
                if (line[1] is None and (learn == 1)) or ((learn == -1) and line[1] is not None):
                    continue
                print(line)
                sz = len(line)
                line = ["none" if (i == 1 and line[i] is None) else line[i] if i < sz else 0.0 for i in range(130)]
                w.writerow(line)
            return data

    def build_with_User_table_for_prog(self, measure="delta", prog="prog", slicer=32, filename="/table.tab"):
        """
        Gera um arquivo csv compatível com o Orange

        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param prog: Um dos possíveis prognosticos do banco: prog, nota, trans, sexo, idade, ano
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :return:
        """
        data = [[user["user"], user[prog]]+[turn[measure] for turn in user["jogada"]][:slicer] for user in self.banco.all()]
        for line in data:
            pass
        return data

if __name__ == '__main__':
    # Learn().report_user_data()
    # Learn().report_user_turn()
    Learn().build_User_table_for_prog(slicer=128, filename="/someeica14.tab", learn=1)  # , learn=True)
