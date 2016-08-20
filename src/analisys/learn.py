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

    def build_User_table_for_prog(self, measure="delta", prog="prog", slicer=32, filename="/table.tab"):
        """
        Gera um arquivo csv compatível com o Orange

        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param prog: Um dos possíveis prognosticos do banco: prog, nota, trans, sexo, idade, ano
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :return:
        """
        data = [[user[prog]]+[turn[measure] for turn in user["jogada"]][:slicer] for user in self.banco.all()]
        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            w = writer(writecsv, delimiter='\t')
            w.writerow('t%d' % t for t, _ in enumerate(data[0]))  # primeiro cabeçalho
            w.writerow('c' if t == 0 else 'd' for t, _ in enumerate(data[0]))
            w.writerow('c' if t == 0 else '' for t, _ in enumerate(data[0]))
            for line in data:
                print(line)
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
    Learn().build_User_table_for_prog()
