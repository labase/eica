# -*- coding: UTF8 -*-
from tinydb import TinyDB, Query
import os
import matplotlib.pyplot as plt


Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S.%f"
JSONDB = os.path.dirname(__file__) + '/eica_new.json'
__author__ = 'carlo'

Y = Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S.%f"
PONTO = "_LINGUA_ _CHAVES_ _MUNDO_ _Chaves_ _ABAS_ _FALA_ _Mundo_ _HOMEM_".split()
CARDS = "_Chaves_ _FALA_ _Mundo_".split()
FILTRO = dict(
    _LINGUA_=lambda item, casa, ponto, valor, plot: [55, 60][bool(valor)] if plot == "_LINGUA_" else -2,
    _CHAVES_=lambda item, casa, ponto, valor, plot: [65, 70][bool(valor)] if plot == "_CHAVES_" else -2,
    _MUNDO_=lambda item, casa, ponto, valor, plot: [75, 80][bool(valor)] if plot == "_MUNDO_" else -2,
    _Chaves_=lambda item, casa, ponto, valor, plot: item if plot == "_Chaves_" else -2,
    _ABAS_=lambda item, casa, ponto, valor, plot: int(casa.split("_")[0])//10 if plot == "_ABAS_" else -2,
    _HOMEM_=lambda item, casa, ponto, valor, plot: [85, 90][bool(valor)] if plot == "_HOMEM_" else -2,
    _FALA_=lambda item, casa, ponto, valor, plot:
    sum(int(val) for val in item.split("_"))//2 if plot == "_FALA_" else -2,
    _Mundo_=lambda item, casa, ponto, valor, plot: item if plot == "_Mundo_" else -2,
    )
DELTA = dict(
    _LINGUA_=lambda delta, plot: delta if plot == "_LINGUA_" else -2,
    _CHAVES_=lambda delta, plot: delta if plot == "_CHAVES_" else -2,
    _MUNDO_=lambda delta, plot: delta if plot == "_MUNDO_" else -2,
    _Chaves_=lambda delta, plot: delta if plot == "_Chaves_" else -2,
    _ABAS_=lambda delta, plot: delta if plot == "_ABAS_" else -2,
    _HOMEM_=lambda delta, plot: delta if plot == "_HOMEM_" else -2,
    _FALA_=lambda delta, plot: delta if plot == "_FALA_" else -2,
    _Mundo_=lambda delta, plot: delta if plot == "_Mundo_" else -2,
    )


class Stats:
    def __init__(self, path=JSONDB):
        self.banco = TinyDB(path)
        self.query = Query()
        
    def list_user_data(self, u_name):
        return self.banco.search(self.query.user == u_name)[0]["jogada"]

    def report_all_user_data(self):
        [self.report_user_data(user) for user in self.new_find_all_users_names()]

    def report_user_data(self, user="tatiane monteiro nascimento"):
        from datetime import datetime as dt
        n, s, m, a = "2016-08-05 10:31:0.031774", "2016-09-05 10:31:0.0", "2016-09-08 01:31:0.0", "2016-09-08 13:31:0.0"
        n, s, m, a = dt.strptime(n, Y), dt.strptime(s, Y), dt.strptime(m, Y), dt.strptime(a, Y)
        data = self.banco.search(self.query.user == user)[0]
        data.pop("jogada")
        hora = dt.strptime(data["hora"], Y)
        turma = "funda" if hora < s else "super" if hora < m else 'medio' if hora < a else "agora"
        data["turma"] = turma
        data = {key: value if value else "NA" for key, value in data.items()}
        # print(data)
        forma = "nome:{user: >52}  idade: {idade: >4}   ano: {ano}     " \
                "genero: {sexo: >16} nota: {nota: >2} prog: {prog: >2}, trans: {trans: >6} {turma} {hora}"
        print(forma.format(**data))

    def new_find_all_users_names(self):
        users = self.banco.search(self.query.user.exists())
        return [a["user"] for a in users]

    def new_delta_plot(self, u_name='wesleyana vitoria aquino de souza'):

        # data = self.banco.new_list_play_data_with_delta(u_name)
        data = self.list_user_data(u_name)
        data = [d for d in data if d["ponto"] in CARDS]
        if not data:
            print(u_name)
            return
        first = [bef.update(dict(first=aft["delta"] - bef["delta"] + 15)) for bef, aft in zip(data, data[1:])]
        data[-1].update(dict(first=-2, second=-2))
        secon = [bef.update(dict(second=(aft["first"] - bef["first"])/10.0))
                 for bef, aft in zip(data, data[1:])]
        data[-1].update(dict(first=-2, second=-2))
        # fig1 = plt.figure()
        fig1, ax = plt.subplots(figsize=(18, 12))
        plt.grid(True)
        plt.subplots_adjust(bottom=0.08, left=.05, right=.95, top=.9, hspace=.35)

        # ax.set_ylim(-1, 1)        # ax.ylim(-5, 5)
        ax.set_ylim(0, 35)        # ax.ylim(-5, 5)
        ax.set_xlim(0, 128)        # ax.ylim(-5, 5)
        ax.set_xlabel('jogadas')
        ax.set_ylabel('tempo de permanência em uma jogada (décimos de segundo)')
        ax.set_title(u_name)
        x = range(len(data)+2)
        # plt.ylim(0, 35)
        # plt.xlim(0, 128)
        # plt.xlabel('jogadas')
        # plt.title(u_name)
        # plt.gca().set_prop_cycle(color=['red', 'green', 'blue', "orange", "magenta", "cyan", "black", 'yellow'])
        for plot in CARDS:
            ax.fill(x, [-2] + [DELTA[d["ponto"]](d["delta"], plot)
                                for d in data] + [-2], label=plot, linewidth=0)
        ax.plot([-100] * len(x), color="black", alpha=.9, label="variação", linewidth=2)
        # plt.plot(x, [-2] + [d["first"] for d in data] + [-2], "magenta")
        # ax.legend(ncol=5, bbox_to_anchor=(0, 1, 1, 3),
        #            loc=3, borderaxespad=1.2, mode="expand")
        ax2 = ax.twinx()
        # ax2.set_xlim(0, min(500, x[-1]))
        # ax2.set_xlim(0, min(500, derivative_data[-1][-1][0]))
        ax2.set_ylim(-1, 1)        # ax.ylim(-5, 5)
        # ax.set_xlim(0, min(1028, derivative_data[-1][-1][0]))
        # ax2.add_collection(lc)
        ax2.set_ylabel('variação do tempo de permanência (segundos)')
        ax2.plot(x, [-2] + [d["second"] for d in data] + [-2], color="black", label="variação")
        # ax2.plot(x, [-2] + [d["second"] for d in data] + [-2], "black",)
        ax.legend(["variação"]+[p for p in CARDS], ncol=5, bbox_to_anchor=(0, 1, 1, 3), loc=3, borderaxespad=1.2, mode="expand")
        fig1.savefig("delta0/%s.jpg" % "_".join(u_name.split()))
        # plt.show()

    def new_simple_plot(self, u_name='wesleyana vitoria aquino de souza'):
        # data = self.banco.new_list_play_data_with_delta(u_name)
        data = self.list_user_data(u_name)
        plt.figure()
        x = [0.] + [float(d["tempo"]) for d in data] + [float(data[-1]["tempo"]) + 1]
        plt.ylim(0, 90)
        plt.xlabel('tempo')
        plt.title(u_name)
        plt.gca().set_prop_cycle(color=['red', 'green', 'blue', "orange", "magenta", "cyan", "black", 'yellow'])
        for plot in PONTO:
            plt.fill(x, [-2] + [FILTRO[d["ponto"]](d["carta"], d["casa"], d["ponto"], d["valor"], plot)
                                for d in data] + [-2], linewidth=0)
        plt.legend([plot for plot in PONTO], ncol=4, bbox_to_anchor=(0, 1, 1, 3),
                   loc=3, borderaxespad=1.2, mode="expand", )
        plt.grid(True)
        plt.subplots_adjust(bottom=0.08, left=.05, right=.96, top=.8, hspace=.35)
        # fig1.savefig("plot/%s.jpg" % "_".join(u_name.split()))
        plt.show()

    def delta_given_users(self, g_users=None):
        prin = g_users if g_users else list(set(self.new_find_all_users_names()))
        for user in prin:
            self.new_delta_plot(user)

    def plot_given_users(self, g_users=None):
        prin = g_users if g_users else list(set(self.new_find_all_users_names()))
        for user in prin:
            self.new_simple_plot(user)

    def plot_item_use_across_games(self):
        u_names = list(set(self.new_find_all_users_names()))
        udata = [self.cross_usage_in_user(u_name) for u_name in u_names]
        udata.sort(key=lambda u: sum(u[1:]))
        ubars = list(zip(*udata))
        labels = ubars.pop(0)
        labels = [" ".join([part.capitalize() if i == 0 else part[:1].capitalize() for i, part in enumerate(name.split())]) for name in labels]
        legend = "Objetos usados,Trans chave/fala,Trans fala/mundo,Trans chave/mundo,Trans total".split(",")
        print(legend)
        # cl = "r g b c m y".split()
        plt.grid(True)
        plt.subplots_adjust(bottom=0.5, left=.05, right=.96, top=0.96, hspace=.35)
        plt.title("Transitividade absoluta de objetos no jogo e total usado")

        x = range(len(ubars[0]))
        plt.xticks(x, labels, rotation='vertical')
        # for i, bar in enumerate(ubars):
        #     plt.bar(x, bar, bottom=None if i == 0 else ubars[i-1], color=cl[i])
        print(ubars[:10])
        plt.bar(x, ubars[0], color="r", label=legend[0], linewidth=0)
        plt.bar(x, ubars[1], bottom=ubars[0], color="g", label=legend[1], linewidth=0)
        plt.bar(x, ubars[2], bottom=[i+j for i, j in zip(ubars[0], ubars[1])], color="b", label=legend[2], linewidth=0)
        plt.bar(x, ubars[3], bottom=[i+j+k for i, j, k in
                                     zip(ubars[0], ubars[1], ubars[2])], color="m", label=legend[3], linewidth=0)
        plt.bar(
            x, ubars[4], bottom=[i+j+k+l for i, j, k, l in
                                 zip(ubars[0], ubars[1], ubars[2], ubars[3])], color="c", label=legend[4], linewidth=0)
        plt.legend(ncol=2, loc="upper left")
        plt.show()
        return

    def cross_usage_in_user(self, u_name):
        data = self.list_user_data(u_name)
        games = "_Chaves_ _FALA_ _Mundo_".split()

        def parse_carta(carta):
            return [carta] if "_" not in carta else carta.split("_")

        items = [set(carta for d in data if d["ponto"] == game for carta in parse_carta(d["carta"])
                     ) for game in games]
        return u_name, len(items[0] | items[1] | items[2]), len(items[0] & items[1]), len(items[1] & items[2]), \
            len(items[0] & items[2]), len(items[0] & items[1] & items[2])


if __name__ == '__main__':
    # Stats().plot_item_use_across_games()
    # Stats().new_delta_plot("Patrick")
    # Stats().report_all_user_data()
    # Stats().new_delta_plot()
    Stats().delta_given_users()
