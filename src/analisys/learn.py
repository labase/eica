# -*- coding: UTF8 -*-
import operator
from tinydb import TinyDB, Query
import os
from csv import writer

# import operator
# from datetime import datetime as dt
# from datetime import timedelta as td
# from time import strftime
# import matplotlib.pyplot as plt
NONE = ""

Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S"
JSONDB = os.path.dirname(__file__) + '/eica_new.json'
JSONSDB = os.path.dirname(__file__) + '/eica_sync.json'
KEYS = {'ano': 3, 'user': 40, 'hora': 20,
        'trans': 8, 'sexo': 12, 'prog': 1, 'nota': 1, 'idade': 2}
KEYLIST = 'user ano idade sexo trans prog nota hora'.split()
FORMAT = " ".join("{key}: {{{key}: <{val}}}".format(key=key, val=KEYS[key]) for key in KEYLIST)
TURN = {'tempo': 12, 'valor': 10, 'casa': 7, 'ponto': 8, 'carta': 12, 'delta': 12}
TURNLIST = 'tempo delta valor casa ponto carta'.split()
TURNFORMAT = " ".join("{key}: {{{key}: <{val}}} ".format(key=key, val=TURN[key]) for key in TURNLIST)
CARDS = "_Chaves_ _FALA_ _Mundo_".split()
GAME_INDEX = dict(_Mundo_=2, _Chaves_=1, _FALA_=3, __A_T_I_V_A__=4)
PROG_INDEX = {key: value for value, key in enumerate("VSFE")}
INDEX_GAME = {key+1: value for key, value in enumerate("_Chaves_ _Mundo_ _FALA_ __A_T_I_V_A__".split())}


class User:
    def __init__(self, user, sexo, idade, ano, hora, nota, prog, trans, jogada):
        self.user, self.sexo, self.idade, self.ano, self.hora, self.nota, self.prog, self.trans, self.jogada =\
            user, sexo, idade, ano, hora, nota, prog, trans, []
        self.load_from_db(jogadas=jogada)
        # time, delta, game = self.resample_user_deltas_games()
        # self.janela_jogadas = [(timer, float(turn) - float(turn0), user.prog, gamer, user.user)
        #                   for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]
        self.iso_classifier = {}
        self.timed_minutia_buckets = [0]*300
        self.minutia_buckets = [0]*40
        self.progclazz_minutia_buckets = [[0 for _ in range(40)] for _ in range(4*3)]
        self.janela_jogadas = []

    def write(self, db):
        attrs = "user, sexo, idade, ano, hora, nota, prog, trans, jogada".split(", ")
        db.insert({k: self.__dict__[k] if k != "jogada" else [jogada.read() for jogada in self.__dict__[k]]
                   for k in dir(self) if k in attrs})

    def load_from_db(self, jogadas):
        self.jogada = [Jogada(**user_data) for user_data in jogadas if "0" not in user_data]
        return self

    def interpolate_deltas(self, delta=1):
        from scipy.interpolate import interp1d  # , splev, splrep, UnivariateSpline
        import numpy as np
        interpolate_deltas = [(jogo.tempo, jogo.delta) for jogo in self.jogada][1:]
        x, y = zip(*interpolate_deltas)
        interpolating_function = interp1d(x, y)
        linear_time_space = np.linspace(x[0], x[-1], (x[-1]-x[0])/delta)

        return linear_time_space, interpolating_function(linear_time_space)

    def interpolate_games(self, delta=1):
        from scipy.interpolate import interp1d
        import numpy as np
        interpolate_deltas = [(jogo.tempo, jogo.ponto) for jogo in self.jogada][1:]
        x, jogo = zip(*interpolate_deltas)
        jogo = ('_',) + jogo + ('_',)
        jogo = [um_jogo if antes_jogo != depois_jogo else antes_jogo
                for antes_jogo, um_jogo, depois_jogo in zip(jogo, jogo[1:], jogo[2:])]
        jogostr = ' '.join(str(a) for a in jogo)
        jogostr = jogostr.replace('_MUNDO_', '_Mundo_')
        jogostr = jogostr.replace('_HOMEM_', '_Mundo_')
        jogostr = jogostr.replace('_ABAS_', '_Chaves_')
        jogostr = jogostr.replace('_CHAVES_', '_Chaves_')
        jogostr = jogostr.replace('_LINGUA_', '_FALA_')
        y = [GAME_INDEX[jogo] for jogo in jogostr.split()]
        interpolating_function = interp1d(x, y, kind='nearest')
        linear_time_space = np.linspace(x[0], x[-1], (x[-1]-x[0])/delta)

        return linear_time_space, interpolating_function(linear_time_space)

    def interpolate_cards(self, delta=1):
        from scipy.interpolate import interp1d
        import numpy as np
        str_index = {}
        index_str = {}

        def get_str_index(token):
            index = len(str_index)
            if token not in str_index:
                str_index[token] = index
                index_str[index] = token
            return index

        interpolate_deltas = [(jogo.tempo, get_str_index(jogo.carta)) for jogo in self.jogada][1:]
        x, jogo = zip(*interpolate_deltas)
        print(str_index)
        print(index_str)
        interpolating_function = interp1d(x, jogo, kind='nearest')
        linear_time_space = np.linspace(x[0], x[-1], (x[-1]-x[0])/delta)

        return linear_time_space, [index_str[int(index)-1] for index in interpolating_function(linear_time_space)]

    def resample_user_deltas_games(self, span=2):
        _, delta = self.interpolate_deltas()
        time, game = self.interpolate_games()
        return [(timer, float(turn) - float(turn0), self.prog, gamer, self.user)
                for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]

    def encontra_minucias_interpolada_em_jogo(self, threshold=32):
        # time, delta, game = self.resample_user_deltas_games()
        data = self.janela_jogadas
        tempo, derivada, clazzes, jogo, user = zip(*data)
        ojogo = jogo[0]
        start = 0
        end = int(min(
            i if a == ojogo != b else 2 ** 100 for i, a, b in zip(tempo, jogo, jogo[1:]))) + 1
        # print(len(self.full_data), ojogo, start, end, [umaclazz for umaclazz in CARDS])
        if (end - start) < threshold:
            return []
        current_game_slice = self.janela_jogadas[:end]
        self.janela_jogadas = self.janela_jogadas[end:]
        return current_game_slice

    def classify_by_normatized_isomorphism(self, data):
        data = data[:3]
        span = (float(max(data)) - float(min(data)))
        data_scale = 29.0 / span if span else 1
        data_floor = float(min(data))
        print("classify_by_normatized_isomorphism", data_scale, data)
        data_isomorphism_lattice = "".join(str(int(((datum - data_floor) * data_scale) // 10))
                                           for datum in data).strip("0") or "0"
        if data_isomorphism_lattice not in self.iso_classifier:
            self.iso_classifier[data_isomorphism_lattice] = data_isomorphism_lattice
        return (data_isomorphism_lattice in self.iso_classifier) and self.iso_classifier[data_isomorphism_lattice]

    def scan_resampled_minutia(self, isoclazz, slicer, user_index, isoclazz_minutia_buckets):
        def headed_data(dat):
            import pywt
            if not dat or len(dat) < slicer:
                return []
            mode = pywt.MODES.sp1

            w = pywt.Wavelet('db3')
            # w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat, w, mode)
            print("wavelet", len(dat), wavelet)
            return list(wavelet)

        while self.janela_jogadas:
            time_slice = self.encontra_minucias_interpolada_em_jogo()
            tempo, data, clazzes, jogo, user = list(zip(*time_slice))
            while len(data) >= slicer:
                print("time_slice", data[:slicer])
                clazz = self.classify_by_normatized_isomorphism(headed_data(data[:slicer]))
                if clazz not in isoclazz:
                    isoclazz.append(clazz)
                if tempo[0] < 300 and user_index[user[0]] < NUS:
                    self.timed_minutia_buckets[int(tempo[0]) // 10] += isoclazz.index(clazz)
                    self.minutia_buckets[isoclazz.index(clazz)] += 1
                if clazz not in isoclazz_minutia_buckets:
                    isoclazz_minutia_buckets[clazz] = 0
                else:
                    isoclazz_minutia_buckets[clazz] += 1
                if clazzes[0]:
                    print("progclazz_minutia_buckets", clazzes[0], isoclazz.index(clazz), jogo[0])
                    self.progclazz_minutia_buckets[3 * PROG_INDEX[clazzes[0]] + int(jogo[0]) - 1][
                        isoclazz.index(clazz)] += 1
                slicer = 3
                data = data[slicer:]
                clazzes = clazzes[slicer:]
                jogo = jogo[slicer:]
                user = user[slicer:]


class Jogada:
    def __init__(self, tempo, delta, ponto, carta, casa, valor, move):
        self.tempo,  self.delta,  self.ponto,  self.carta,  self.casa,  self.valor,  self.move =\
            tempo, delta, ponto, carta, casa, valor, move

    def read(self):
        attrs = "tempo, delta, ponto, carta, casa, valor, move".split(", ")
        return {k: self.__dict__[k] for k in dir(self) if k in attrs}

    def update(self, **kwargs):
        attrs = "tempo, delta, ponto, carta, casa, valor, move".split(", ")
        [setattr(self, attr, value) for attr, value in kwargs.items() if attr in attrs]
        return self


class Learn:
    def __init__(self, path=JSONDB):
        self.banco = TinyDB(path)
        self.query = Query()
        self.full_data = []
        self.data = []
        self.user = []
        self.iso_classes = []
        self.progclazz_minutia_buckets = {}
        self.user_timed_minutia_buckets = {}
        self.isoclazz_minutia_buckets = {}
        self.user_minutia_buckets = {}
        self.iso_classifier = {}

    def write_db(self, path=JSONSDB):
        sdb = TinyDB(path)
        [user.write(sdb) for user in self.user]
        return self

    def load_from_db(self):
        self.user = [User(**user_data) for user_data in self.banco.all()]
        return self

    def replace_resampled_user_deltas_games_cards(self):
        def interpolate(user):
            try:
                if len(user.jogada) < 1:
                    return [[]]*4
                _, delta = user.interpolate_deltas()
                x, game = user.interpolate_games()
                _, cards = user.interpolate_cards()
                return zip(x, delta, game, cards)
            except ValueError as _:
                return [[0]*4]
        [user.jogada[index].update(tempo=tempo, delta=delta, ponto=game, carta=card) for user in self.user
         for index, (tempo, delta, game, card) in enumerate(interpolate(user)) if index < len(user.jogada) > 2]
        return self

    def resample_user_deltas_games(self, _=2):
        _, delta = self.user[2].interpolate_deltas()
        x, game = self.user[2].interpolate_games()
        return x, delta, game

    def resample_user_deltas(self, _=2):
        import matplotlib.pyplot as plt
        x, y = self.user[2].interpolate_games()
        plt.plot(x[:256], y[:256])
        # plt.plot(x,y,xl,s2(xl[::-1]), xl, ynew)
        plt.legend(['data'], loc='best')
        plt.show()

    def report_user_data(self):
        values = self.banco.all()
        print(len(values))
        # dem = ["user", "idade", "sexo", "ano", "hora"]
        print(FORMAT)
        # print(FORMAT.format(**{key: val for key, val in values[3].items() if key != "jogada"}))
        print({key: val or "#" for key, val in values[3].items() if key != "jogada"})
        for i, name in enumerate(values):
            format_string = "{:3d} " + FORMAT
            data = {key: val or "#" for key, val in name.items() if key != "jogada"}
            print(format_string.format(i, **data))

    def report_user_turn(self, u_name="LARISSA"):
        user = self.banco.search(self.query.user == u_name)[0]
        print(len(user["jogada"][0]))
        # dem = ["user", "idade", "sexo", "ano", "hora"]
        print(user["jogada"][0])
        print(TURNFORMAT.format(**{key: val for key, val in user["jogada"][0].items()}))
        # return
        # print({key: val or "#" for key, val in values[3].items() if key != "jogada"})
        for i, name in enumerate(user["jogada"]):
            format_string = "{:3d} " + TURNFORMAT
            data = {key: val or "#" for key, val in name.items()}
            print(format_string.format(i, **data))

    def build_user_table_for_minucia(self, measure="delta", prog="prog", slicer=128, filename="/minucias.tab",
                                     learn=False, threshold=16):
        """
        Gera um arquivo csv compatível com o Orange

        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param prog: Um dos possíveis prognosticos do banco: prog, nota, trans, sexo, idade, ano
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :param learn: imprime somente dados para aprendizagem
        :param threshold: contagem mínima
        :return:
        """

        def sigla(name, order=""):
            return ' '.join(n.capitalize() if i == 0 else n.capitalize()[0] + "."
                            for i, n in enumerate(name.split())) + name[-1] + str(order)
        self.full_data = [(float(turn[measure]) - float(turn0[measure]), user[prog], turn["ponto"], user["user"])
                          for user in self.banco.all()
                          for turn, turn0 in zip(user["jogada"][1:slicer], user["jogada"][:slicer])]
        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            w = writer(writecsv, delimiter='\t')
            w.writerow(['n', 'CL'] + ['t%d' % t for t in range(32)])  # primeiro cabeçalho
            print('cabs', len(self.full_data), len((['n', 'CL'] + ['t%d' % t for t in range(32)])))

            w.writerow(['d'] + ['d' if t == 0 else 'c' for t in range(33)])
            w.writerow(['m'] + ['c' if t == 0 else '' for t in range(33)])
            while self.full_data:

                def encontra_minucia():
                    data = self.full_data[:32]
                    derivada, clazzes, jogo, user = zip(*data)
                    jogo = ('_',) + jogo + ('_',)
                    jogo = [um_jogo if antes_jogo != depois_jogo else antes_jogo
                            for antes_jogo, um_jogo, depois_jogo in zip(jogo, jogo[1:], jogo[2:])]
                    jogostr = ' '.join(str(a) for a in jogo)
                    jogostr = jogostr.replace('_MUNDO_', '_Mundo_')
                    jogostr = jogostr.replace('_ABAS_', '_Chaves_')
                    jogostr = jogostr.replace('_CHAVES_', '_Chaves_')
                    jogostr = jogostr.replace('_LINGUA_', '_FALA_')
                    jogo = jogostr.split()
                    ojogo = jogo[0]
                    start = 0
                    end = min(31, min(
                        i if a == ojogo != b else 2 ** 100 for i, (a, b) in enumerate(zip(jogo[:32], jogo[1:32])))) + 1
                    print(len(self.full_data), ojogo, start, end, [(jogostr.count(umaclazz), umaclazz)
                                                                   for umaclazz in CARDS], jogostr[:80])
                    self.full_data = self.full_data[end:]
                    clazz = ojogo+clazzes[start] if clazzes[start] else NONE
                    if (end - start) < threshold:
                        return None
                    return [ojogo[1]+" "+sigla(user[start]), clazz] + [d if i < end - start else ""
                                                                       for i, d in enumerate(derivada[:32])]

                minucia = encontra_minucia()
                if not minucia or learn and minucia[1] == NONE or (learn is None) and minucia[1] != NONE:
                    continue

                row = [minucia.pop(0),  minucia.pop(0)] + minucia
                print(row)
                sz = len(row)

                if sz < 3:
                    continue
                row = ["none" if (i == 1 and row[i] is None) else row[i] if i < sz else 0.0 for i in range(34)]
                print(len(row))
                w.writerow(row)
            return self.full_data

    def build_user_table_for_transitive_minucia(self, measure="delta", prog="prog", slicer=128,
                                                filename="/trasitiveminucias.tab", learn=False):
        """
        Gera um arquivo csv compatível com o Orange.

        Computa o uso transitivo de objetos ao longo do chaveamento dos jogos.

        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param prog: Um dos possíveis prognosticos do banco: prog, nota, trans, sexo, idade, ano
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :param learn: imprime somente dados para aprendizagem
        :return:
        """

        self.full_data = [(float(turn[measure]) - float(turn0[measure]), user[prog], turn["ponto"], user["user"])
                          for user in self.banco.all()
                          for turn, turn0 in zip(user["jogada"][1:slicer], user["jogada"][:slicer])]
        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            w = writer(writecsv, delimiter='\t')
            w.writerow(['n', 'CL'] + ['t%d' % t for t in range(32)])  # primeiro cabeçalho
            print('cabs', len(self.full_data), len((['n', 'CL'] + ['t%d' % t for t in range(32)])))

            w.writerow(['d'] + ['d' if t == 0 else 'c' for t in range(33)])
            w.writerow(['m'] + ['c' if t == 0 else '' for t in range(33)])
            while self.full_data:

                minucia = self._encontra_minucia()
                if not minucia or learn and minucia[1] == NONE or (learn is None) and minucia[1] != NONE:
                    continue

                row = [minucia.pop(0),  minucia.pop(0)] + minucia
                print(row)
                sz = len(row)

                if sz < 3:
                    continue
                row = ["none" if (i == 1 and row[i] is None) else row[i] if i < sz else 0.0 for i in range(34)]
                print(len(row))
                w.writerow(row)
            return self.full_data

    def build_user_table_for_prog(self, measure="delta", prog="prog", slicer=32, filename="/table.tab", learn=False):
        """
        Gera um arquivo csv compatível com o Orange

        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param prog: Um dos possíveis prognosticos do banco: prog, nota, trans, sexo, idade, ano
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :param learn: elimina linhas sem prognóstico
        :return:
        """

        def sigla(name):
            return ' '.join(n.capitalize() if i == 0 else n.capitalize()[0] + "."
                            for i, n in enumerate(name.split())) + name[-1]

        data = [
            [sigla(user["user"]), user[prog]] +
            [float(turn[measure]) - float(turn0[measure]) for turn, turn0 in
             zip(user["jogada"][1:slicer], user["jogada"][:slicer])] for user in self.banco.all()]
        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            print(JSONDB, self.banco.all())
            w = writer(writecsv, delimiter='\t')
            w.writerow(['n', 'CL'] + ['t%d' % t for t in range(32)])  # primeiro cabeçalho
            w.writerow(['d'] + ['d' if t == 0 else 'c' for t in range(32)])
            w.writerow(['m'] + ['c' if t == 0 else '' for t in range(32)])
            for line in data:
                if line[1] is None and learn:
                    continue
                print(line)
                sz = len(line)
                line = ["" if (i == 1 and line[i] is None) else line[i] if i < sz else 0.0 for i in range(130)]
                w.writerow(line)
            return data

    def build_user_table_as_timeseries(self, measure="delta", slicer=128, filename="/timeseries.tab"):
        """
        Gera um arquivo csv compatível com o Orange

        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :return:
        """

        def sigla(name):
            return ' '.join(n.capitalize() if i == 0 else n.capitalize()[0] + "."
                            for i, n in enumerate(name.split())) + name[-1]

        data = [
            [sigla(user["user"]), 'c', ''] +
            [float(turn[measure]) - float(turn0[measure]) for turn, turn0 in
             zip(user["jogada"][1:slicer], user["jogada"][:slicer])] for user in self.banco.all()]
        data = [line + [0.0]*(slicer - len(line)) for line in data]
        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            print(JSONDB, self.banco.all())
            w = writer(writecsv, delimiter='\t')
            data = zip(*data)
            for line in data:
                print(line)
                w.writerow(line)
            return data

    def build_derivative_minutia_as_timeseries(self, measure="delta", prog="prog", slicer=16,
                                               filename="/minutiatimeseries.tab", threshold=6):
        """
        Gera um arquivo csv compatível com o Orange para analise harmônica de minucias de segunda ordem

        :param prog: Um dos possíveis prognosticos do banco: prog, nota, trans, sexo, idade, ano
        :param threshold:
        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :return:
        """

        def headed_data(dat, index):
            import pywt
            if not dat or len(dat) < slicer:
                return []
            print(len(dat))
            mode = pywt.MODES.sp1

            wav = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat[2:], wav, mode)
            print(wavelet)
            return ["%s%0d3" % (dat[0], index), "c", ""] + list(wavelet)
        span = slicer*16

        self.full_data = [(float(turn[measure]) - float(turn0[measure]), user[prog], turn["ponto"], user["user"])
                          for user in self.banco.all()
                          for turn, turn0 in zip(user["jogada"][1:span], user["jogada"][:span])]
        data = [headed_data(self._encontra_minucia(slicer=slicer, threshold=threshold), i)
                for i in range(span) if self.full_data]
        data = [line for line in data if line]
        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            w = writer(writecsv, delimiter='\t')
            data = zip(*data)
            for line in data:
                print(line)
                w.writerow(line)
            return data

    def _encontra_minucia(self, threshold=32, slicer=64):

        def sigla(name, order=""):
            return ' '.join(n.capitalize() if i == 0 else n.capitalize()[0] + "."
                            for i, n in enumerate(name.split())) + name[-1] + str(order)
        data = self.full_data[:slicer]
        derivada, clazzes, jogo, user = zip(*data)
        jogostr = ' '.join(str(a) for a in jogo)
        jogostr = jogostr.replace('_MUNDO_', '_Mundo_')
        jogostr = jogostr.replace('_HOMEM_', '_Mundo_')
        jogostr = jogostr.replace('_ABAS_', '_Chaves_')
        jogostr = jogostr.replace('_CHAVES_', '_Chaves_')
        jogostr = jogostr.replace('_LINGUA_', '_FALA_')
        jogo = jogostr.split()
        jogo = ['_'] + jogo + ['_']
        jogo = [um_jogo if antes_jogo != depois_jogo else antes_jogo
                for antes_jogo, um_jogo, depois_jogo in zip(jogo, jogo[1:], jogo[2:])]
        ojogo = jogo[0]
        start = 0
        end = min(slicer-1, min(
            i if a == ojogo != b else 2 ** 100 for i, (a, b) in enumerate(zip(jogo[:slicer], jogo[1:slicer])))) + 1
        print(len(self.full_data), ojogo, start, end, [(jogostr.count(umaclazz), umaclazz)
                                                       for umaclazz in CARDS], jogostr[:80])
        self.full_data = self.full_data[end:]
        clazz = ojogo + clazzes[start] if clazzes[start] else NONE
        if (end - start) < threshold:
            return []
        return [ojogo[1] + " " + sigla(user[start]), clazz] + list(derivada[:end]) + [0.0]*(slicer-end)

    def _encontra_minucia_interpolada(self, threshold=32, slicer=64):

        def sigla(name, order=""):
            return ' '.join(n.capitalize() if i == 0 else n.capitalize()[0] + "."
                            for i, n in enumerate(name.split())) + name[-1] + str(order)
        data = self.full_data[:slicer]
        tempo, derivada, clazzes, jogo, user = zip(*data)
        ojogo = jogo[0]
        start = 0
        end = min(slicer-1, min(
            i if a == ojogo != b else 2 ** 100 for i, a, b in zip(tempo, jogo[:slicer], jogo[1:slicer]))) + 1
        # print(len(self.full_data), ojogo, start, end, [umaclazz for umaclazz in CARDS])
        self.full_data = self.full_data[end:]
        ojogo = INDEX_GAME[ojogo]
        clazz = "_%s_%s_" % (ojogo[1], clazzes[start]) if clazzes[start] else "_%s_._" % ojogo[1]
        if (end - start) < threshold:
            return []
        return [sigla(user[start], clazz), clazz] + list(derivada[:end]) + [0.0]*(slicer-end)

    def normatize_for_isomorphic_classification(self, data):
        span = (float(max(data)) - float(min(data)))
        data_scale = 26.0 / span if span else 1
        data_floor = float(min(data))
        print("normatize", data_scale, data)
        data_isomorphism_lattice = "".join(str(int(((datum - data_floor) * data_scale) // 10))
                                           for datum in data).strip("0") or "000000"
        self.iso_classes.append(data_isomorphism_lattice)
        return data_isomorphism_lattice

    def build_interpolated_derivative_minutia(
            self, slicer=16, filename="/interpolatedminutia.tab", threshold=6, span=0):
        """
        Gera um arquivo tab do Orange para analise harmônica de minucias de segunda ordem interploadas no tempo.

        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :param threshold: elimina linhas sem prognóstico
        :param span: intervalo onde a pesquisa da minucia será investigada
        :return:
        """

        def headed_data(dat, index):
            import pywt
            if not dat or len(dat) < slicer:
                return []
            print(len(dat))
            mode = pywt.MODES.sp1

            wav = pywt.Wavelet('db3')
            # w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat[2:], wav, mode)
            print(wavelet)
            return ["%s%0d3" % (dat[0], index), dat[1]] + list(wavelet)
        span = span or slicer*64
        time, delta, game = self.resample_user_deltas_games()

        self.full_data = [(timer, float(turn) - float(turn0), user.prog, gamer, user.user)
                          for user in self.user
                          for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]
        data = [headed_data(self._encontra_minucia_interpolada(slicer=slicer, threshold=threshold), i)
                for i in range(span) if self.full_data]
        data = [[name, self.normatize_for_isomorphic_classification(dat[:threshold])] + dat
                for name, _, *dat in data if name]

        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            w = writer(writecsv, delimiter='\t')
            w.writerow(['n', 'CL'] + ['t%d' % t for t in range(slicer)])  # primeiro cabeçalho
            print('cabs', len(self.full_data), len((['n', 'CL'] + ['t%d' % t for t in range(32)])))

            w.writerow(['d'] + ['d' if t == 0 else 'c' for t in range(slicer+1)])
            w.writerow(['m'] + ['c' if t == 0 else '' for t in range(slicer+1)])
            for line in data:
                print(line)
                w.writerow(line)
            print(len(set(self.iso_classes)))
            print(set(self.iso_classes))
            return data


class Track:
    def __init__(self, path=JSONDB):
        self.banco = TinyDB(path)
        self.query = Query()
        self.full_data = []
        self.data = []
        self.user = []
        self.iso_classes = []
        self.progclazz_minutia_buckets = {}
        self.user_timed_minutia_buckets = {}
        self.isoclazz_minutia_buckets = {}
        self.user_minutia_buckets = {}
        self.iso_classifier = {}

    def resample_user_deltas_games(self, _=2):
        _, delta = self.user[2].interpolate_deltas()
        x, game = self.user[2].interpolate_games()
        return x, delta, game

    def scan_full_data_for_minutia_count_in_user_and_games(
            self, slicer=16, span=4):
        """
        Gera um arquivo tab do Orange para analise harmônica de minucias de segunda ordem interploadas no tempo.

        :param slicer: recorta eos dados neste tamanho
        :param span: intervalo onde a pesquisa da minucia será investigada
        :return:
        """

        def headed_data(dat):
            import pywt
            if not dat or len(dat) < slicer:
                return []
            mode = pywt.MODES.sp1

            w = pywt.Wavelet('db3')
            # w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat, w, mode)
            print("wavelet", len(dat), wavelet)
            return list(wavelet)
        time, delta, game = self.resample_user_deltas_games()
        user_index = {user.user: index for index, user in enumerate(self.user)}
        self.user_timed_minutia_buckets = [[0 for _ in range(300)] for _ in range(NUS)]
        self.user_minutia_buckets = [[0 for _ in range(40)] for _ in range(70)]
        self.progclazz_minutia_buckets = [[0 for _ in range(40)] for _ in range(4*3)]
        self.isoclazz_minutia_buckets = {i_clazz: 0 for i_clazz in set(self.iso_classes)}
        self.iso_classifier = {clazz: clazz for clazz in set(self.iso_classes)}

        self.full_data = [(timer, float(turn) - float(turn0), user.prog, gamer, user.user)
                          for user in self.user
                          for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]
        print("len(self.full_data)", len(self.full_data), self.full_data[0], self.iso_classifier)
        isoclazz = []
        while self.full_data:
            time_slice = self._encontra_minucias_interpolada_em_jogo()
            tempo, data, clazzes, jogo, user = list(zip(*time_slice))
            while len(data) >= slicer:
                print("time_slice", data[:slicer])
                clazz = self.classify_by_normatized_isomorphism(headed_data(data[:slicer]))
                if clazz not in isoclazz:
                    isoclazz.append(clazz)
                if tempo[0] < 300 and user_index[user[0]] < NUS:
                    self.user_timed_minutia_buckets[user_index[user[0]]][int(tempo[0])//10] += isoclazz.index(clazz)
                    self.user_minutia_buckets[user_index[user[0]]][isoclazz.index(clazz)] += 1
                if clazz not in self.isoclazz_minutia_buckets:
                    self.isoclazz_minutia_buckets[clazz] = 0
                else:
                    self.isoclazz_minutia_buckets[clazz] += 1
                if clazzes[0]:
                    print("progclazz_minutia_buckets", clazzes[0], isoclazz.index(clazz), jogo[0])
                    self.progclazz_minutia_buckets[3*PROG_INDEX[clazzes[0]]+int(jogo[0])-1][isoclazz.index(clazz)] += 1
                slicer = 3
                data = data[slicer:]
                clazzes = clazzes[slicer:]
                jogo = jogo[slicer:]
                user = user[slicer:]
        print(len(self.isoclazz_minutia_buckets), self.isoclazz_minutia_buckets)
        print({oc: sum(1 for c in self.iso_classes if c == oc) for oc in set(self.iso_classes)})
        print(self.progclazz_minutia_buckets)
        print([u.user for u in self.user[:NUS]])
        print(self.user_minutia_buckets)
        for user, index in user_index.items():
            print(user, self.user_minutia_buckets[index])
        # self.plot_derivative_minutia_by_prognostics_games()
        self.plot_derivative_minutia_by_user_prognostics_games()
        print(sum(count for user in self.user_minutia_buckets for count in user))
        print(sum(1 for user in self.user_minutia_buckets if any(user)))
        return
        # plt.imshow(zi, vmin=min(z), vmax=max(z), origin='lower',
        #            extent=[min(x), max(x), min(y), max(y)])
        # plt.scatter(x, y, c=z)
        # plt.colorbar()
        # plt.show()

    def scan_for_minutia_count_in_user_and_games(
            self, slicer=16):
        """
        Gera um arquivo tab do Orange para analise harmônica de minucias de segunda ordem interploadas no tempo.

        :param slicer: recorta eos dados neste tamanho
        :return:
        """
        user_index = {user.user: index for index, user in enumerate(self.user)}
        self.user_timed_minutia_buckets = [[0 for _ in range(300)] for _ in range(NUS)]
        self.user_minutia_buckets = [[0 for _ in range(40)] for _ in range(70)]
        self.progclazz_minutia_buckets = [[0 for _ in range(40)] for _ in range(4*3)]
        self.isoclazz_minutia_buckets = {i_clazz: 0 for i_clazz in set(self.iso_classes)}
        self.iso_classifier = {clazz: clazz for clazz in set(self.iso_classes)}
        isoclazz = []
        for user in self.user:
            user.scan_resampled_minutia(isoclazz, slicer, user, user_index, self.isoclazz_minutia_buckets)
        print(len(self.isoclazz_minutia_buckets), self.isoclazz_minutia_buckets)
        print({oc: sum(1 for c in self.iso_classes if c == oc) for oc in set(self.iso_classes)})
        print(self.progclazz_minutia_buckets)
        print([u.user for u in self.user[:NUS]])
        print(self.user_minutia_buckets)
        for user, index in user_index.items():
            print(user, self.user_minutia_buckets[index])
        # self.plot_derivative_minutia_by_prognostics_games()
        # self.plot_derivative_minutia_by_user_prognostics_games()
        print(sum(count for user in self.user_minutia_buckets for count in user))
        print(sum(1 for user in self.user_minutia_buckets if any(user)))
        return
        # plt.imshow(zi, vmin=min(z), vmax=max(z), origin='lower',
        #            extent=[min(x), max(x), min(y), max(y)])
        # plt.scatter(x, y, c=z)
        # plt.colorbar()
        # plt.show()

    def normatize_for_isomorphic_classification(self, data):
        span = (float(max(data)) - float(min(data)))
        data_scale = 26.0 / span if span else 1
        data_floor = float(min(data))
        print("normatize", data_scale, data)
        data_isomorphism_lattice = "".join(str(int(((datum - data_floor) * data_scale) // 10))
                                           for datum in data).strip("0") or "000000"
        self.iso_classes.append(data_isomorphism_lattice)
        return data_isomorphism_lattice

    def classify_by_normatized_isomorphism(self, data):
        data = data[:3]
        span = (float(max(data)) - float(min(data)))
        data_scale = 27.0 / span if span else 1
        data_floor = float(min(data))
        print("classify_by_normatized_isomorphism", data_scale, data)
        data_isomorphism_lattice = "".join(str(int(((datum - data_floor) * data_scale) // 10))
                                           for datum in data).strip("0") or "0"
        if data_isomorphism_lattice not in self.iso_classifier:
            self.iso_classifier[data_isomorphism_lattice] = data_isomorphism_lattice
        return (data_isomorphism_lattice in self.iso_classifier) and self.iso_classifier[data_isomorphism_lattice]

    def load_from_db(self):
        self.user = [User(**user_data) for user_data in self.banco.all()]
        return self

    def _encontra_minucia_interpolada(self, threshold=32, slicer=64):

        def sigla(name, order=""):
            return ' '.join(n.capitalize() if i == 0 else n.capitalize()[0] + "."
                            for i, n in enumerate(name.split())) + name[-1] + str(order)
        data = self.full_data[:slicer]
        tempo, derivada, clazzes, jogo, user = zip(*data)
        ojogo = jogo[0]
        start = 0
        end = min(slicer-1, min(
            i if a == ojogo != b else 2 ** 100 for i, a, b in zip(tempo, jogo[:slicer], jogo[1:slicer]))) + 1
        # print(len(self.full_data), ojogo, start, end, [umaclazz for umaclazz in CARDS])
        self.full_data = self.full_data[end:]
        ojogo = INDEX_GAME[ojogo]
        clazz = "_%s_%s_" % (ojogo[1], clazzes[start]) if clazzes[start] else "_%s_._" % ojogo[1]
        if (end - start) < threshold:
            return []
        return [sigla(user[start], clazz), clazz] + list(derivada[:end]) + [0.0]*(slicer-end)

    def _encontra_minucias_interpolada_em_jogo(self, threshold=32):
        data = self.full_data
        tempo, derivada, clazzes, jogo, user = zip(*data)
        ojogo = jogo[0]
        start = 0
        end = int(min(
            i if a == ojogo != b else 2 ** 100 for i, a, b in zip(tempo, jogo, jogo[1:]))) + 1
        # print(len(self.full_data), ojogo, start, end, [umaclazz for umaclazz in CARDS])
        if (end - start) < threshold:
            return []
        current_game_slice = self.full_data[:end]
        self.full_data = self.full_data[end:]
        return current_game_slice

    def plot_derivative_minutia_by_prognostics_games(self):
        import numpy as np
        import matplotlib.pyplot as plt
        import scipy.interpolate
        from mpl_toolkits.mplot3d import Axes3D
        assert Axes3D
        from matplotlib import cm
        # Generate data:
        x, y, z = zip(*[(x, y, self.progclazz_minutia_buckets[x][y]) for y in range(12) for x in range(4 * 3)])
        # x, y, z = list(x), list(y), list(z)
        # Set up a regular grid of interpolation points
        # xi, yi = np.linspace(min(x), max(x), 12), np.linspace(min(y), max(y), 12)
        xi, yi = np.linspace(0, 12, 12), np.linspace(0, 12, 12)
        xi, yi = np.meshgrid(xi, yi)
        # Interpolate
        rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
        zi = rbf(xi, yi)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        labels = "v.s. chaves,v.s. mundo,v.s. fala,s.m. chaves,s.m. mundo,s.m. fala," \
                 "f.s. chaves,f.s. mundo,f.s. fala,e.s. chaves,e.s. mundo,e.s. fala,".split(",")
        # ax.plot_trisurf(x, y, zi, cmap=cm.jet, linewidth=0.2)
        plt.xticks(x, labels, rotation='vertical')
        ax.plot_surface(xi[::-1], yi, zi, rstride=1, cstride=1, color='b', cmap=cm.coolwarm,
                        linewidth=0, antialiased=False, shade=False)
        plt.show()

    def plot_derivative_minutia_by_user_prognostics_games(self):
        import numpy as np
        import matplotlib.pyplot as plt
        import scipy.interpolate
        from mpl_toolkits.mplot3d import Axes3D
        assert Axes3D
        from matplotlib import cm
        # Generate data:
        x, y, z = zip(*[(x, y, self.user_timed_minutia_buckets[x][y]) for y in range(300) for x in range(NUS)])
        # x, y, z = list(x), list(y), list(z)
        # Set up a regular grid of interpolation points
        # xi, yi = np.linspace(min(x), max(x), 12), np.linspace(min(y), max(y), 12)
        xi, yi = np.linspace(0, 30, 30), np.linspace(0, NUS, NUS)
        xi, yi = np.meshgrid(xi, yi)
        # Interpolate
        rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
        zi = rbf(xi, yi)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        # labels = "v.s. chaves,v.s. mundo,v.s. fala,s.m. chaves,s.m. mundo,s.m. fala," \
        #          "f.s. chaves,f.s. mundo,f.s. fala,e.s. chaves,e.s. mundo,e.s. fala,".split(",")
        # ax.plot_trisurf(x, y, zi, cmap=cm.jet, linewidth=0.2)
        # plt.xticks(x, labels, rotation='vertical')
        ax.plot_surface(xi[::-1], yi, zi, rstride=1, cstride=1, color='b', cmap=cm.coolwarm,
                        linewidth=0, antialiased=False, shade=False)
        plt.show()

NUS = 30


def _notmain():
    # Learn().report_user_data()
    # Learn().report_user_turn()
    # Learn().build_User_table_for_prog(slicer=128, learn=False, filename="/fullderivative.tab")
    # Learn().build_user_table_for_minucia(slicer=128, filename="/fullminucias.tab", learn=False)
    # Learn().build_user_table_for_minucia(slicer=1024, threshold=16, filename="/largeminucias.tab", learn=True)
    # Learn().train_classify_wnn()
    # Learn().plot_derivative_minutia()
    # Learn().build_User_table_as_timeseries()
    # Learn().build_derivative_minutia_as_timeseries(filename="/minutia16timeseries.tab")
    # Learn().load_from_db().build_interpolated_derivative_minutia(slicer=4, threshold=2, span=256)
    pass


if __name__ == '__main__':
    Track().load_from_db().scan_full_data_for_minutia_count_in_user_and_games(slicer=6, span=1256)
    # Learn().load_from_db().replace_resampled_user_deltas_games_cards().write_db()
    # Learn().load_from_db().build_interpolated_derivative_minutia_as_timeseries(slicer=12, threshold=8)
    # Learn().load_from_db().resample_user_deltas()
