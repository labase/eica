from clean import Banco
import matplotlib.pyplot as plt
__author__ = 'carlo'

Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S"
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
    def __init__(self):
        self.banco = Banco()

    def new_delta_plot(self, u_name='wesleyana vitoria aquino de souza'):
        # data = self.banco.new_list_play_data_with_delta(u_name)
        data = self.banco.new_list_play_data_adjusted_with_delta(u_name)
        data = [d for d in data if d["ponto"] in CARDS]
        first = [bef.update(dict(first=aft["delta"] - bef["delta"] + 15)) for bef, aft in zip(data, data[1:])]
        data[-1].update(dict(first=-2, second=-2))
        secon = [bef.update(dict(second=aft["first"] - bef["first"] + 25))
                 for bef, aft in zip(data, data[1:])]
        data[-1].update(dict(first=-2, second=-2))
        fig1 = plt.figure()
        x = range(len(data)+2)
        plt.ylim(0, 35)
        plt.xlim(0, 128)
        plt.xlabel('jogadas')
        plt.title(u_name)
        plt.gca().set_prop_cycle(color=['red', 'green', 'blue', "orange", "magenta", "cyan", "black", 'yellow'])
        for plot in CARDS:
            plt.fill(x, [-2] + [DELTA[d["ponto"]](d["delta"], plot)
                                for d in data] + [-2], linewidth=0)
        # plt.plot(x, [-2] + [d["first"] for d in data] + [-2], "magenta")
        plt.plot(x, [-2] + [d["second"] for d in data] + [-2], "black",)
        plt.legend(["SEG"]+[plot for plot in CARDS], ncol=5, bbox_to_anchor=(0, 1, 1, 3),
                   loc=3, borderaxespad=1.2, mode="expand")
        plt.grid(True)
        plt.subplots_adjust(bottom=0.08, left=.05, right=.96, top=.9, hspace=.35)
        fig1.savefig("delta/%s.jpg" % "_".join(u_name.split()))
        # plt.show()

    def new_simple_plot(self, u_name='wesleyana vitoria aquino de souza'):
        # data = self.banco.new_list_play_data_with_delta(u_name)
        data = self.banco.new_list_play_data_adjusted_with_delta(u_name)
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
        prin = g_users if g_users else list(set(self.banco.new_find_all_users_names()))
        for user in prin:
            self.new_delta_plot(user)

    def plot_given_users(self, g_users=None):
        prin = g_users if g_users else list(set(self.banco.new_find_all_users_names()))
        for user in prin:
            self.new_simple_plot(user)

    def plot_item_use_across_games(self):
        u_names = list(set(self.banco.new_find_all_users_names()))
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
        data = self.banco.new_list_play_data_with_delta(u_name)
        games = "_Chaves_ _FALA_ _Mundo_".split()

        def parse_carta(carta):
            return [carta] if "_" not in carta else carta.split("_")

        items = [set(carta for d in data if d["ponto"] == game for carta in parse_carta(d["carta"])
                     ) for game in games]
        return u_name, len(items[0] | items[1] | items[2]), len(items[0] & items[1]), len(items[1] & items[2]), \
            len(items[0] & items[2]), len(items[0] & items[1] & items[2])


if __name__ == '__main__':
    # Stats().plot_item_use_across_games()
    # Stats().new_delta_plot()
    # Stats().new_delta_plot()
    Stats().delta_given_users()
