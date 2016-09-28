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
KEYS = {'ano': 3, 'user': 40, 'hora': 20,
        'trans': 8, 'sexo': 12, 'prog': 1, 'nota': 1, 'idade': 2}
KEYLIST = 'user ano idade sexo trans prog nota hora'.split()
FORMAT = " ".join("{key}: {{{key}: <{val}}}".format(key=key, val=KEYS[key]) for key in KEYLIST)
TURN = {'tempo': 12, 'valor': 10, 'casa': 7, 'ponto': 8, 'carta': 12, 'delta': 12}
TURNLIST = 'tempo delta valor casa ponto carta'.split()
TURNFORMAT = " ".join("{key}: {{{key}: <{val}}} ".format(key=key, val=TURN[key]) for key in TURNLIST)
CARDS = "_Chaves_ _FALA_ _Mundo_".split()
GAME_INDEX = dict(_Mundo_=1, _Chaves_=2, _FALA_=3)
INDEX_GAME = {key+1: value for key, value in enumerate("_Mundo_ _Chaves_= _FALA_".split())}


class User:
    def __init__(self, user, sexo, idade, ano, hora, nota, prog, trans, jogada):
        self.user, self.sexo, self.idade, self.ano, self.hora, self.nota, self.prog, self.trans, self.jogada =\
            user, sexo, idade, ano, hora, nota, prog, trans, []
        self.load_from_db(jogadas=jogada)

    def load_from_db(self, jogadas):
        self.jogada = [Jogada(**user_data) for user_data in jogadas if "0" not in user_data]
        return self

    def interpolate_deltas(self, delta=1):
        from scipy.interpolate import interp1d, splev, splrep, UnivariateSpline
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


class Jogada:
    def __init__(self, tempo, delta, ponto, carta, casa, valor, move):
        self.tempo,  self.delta,  self.ponto,  self.carta,  self.casa,  self.valor,  self.move =\
            tempo, delta, ponto, carta, casa, valor, move


class Learn:
    def __init__(self, path=JSONDB):
        self.banco = TinyDB(path)
        self.query = Query()
        self.full_data = []
        self.data = []
        self.user = []
        self.iso_classes = []

    def load_from_db(self):
        self.user = [User(**user_data) for user_data in self.banco.all()]
        return self

    def resample_user_deltas_games(self, new_delta=2):
        _, delta = self.user[2].interpolate_deltas()
        x, game = self.user[2].interpolate_games()
        return x, delta, game

    def resample_user_deltas(self, new_delta=2):
        x, y = self.user[2].interpolate_games()
        import matplotlib.pyplot as plt
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
        print(len(self.full_data), ojogo, start, end, [umaclazz
                                                       for umaclazz in CARDS])
        self.full_data = self.full_data[end:]
        ojogo = INDEX_GAME[ojogo]
        clazz = "_%s_%s_" % (ojogo[1], clazzes[start]) if clazzes[start] else "_%s_._" % ojogo[1]
        stubber = slicer-end if slicer-end > 0 else 0
        if (end - start) < threshold:
            return []
        return [sigla(user[start], clazz), clazz] + list(derivada[:end]) + [0.0]*(slicer-end)

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
        games = "_Chaves_ _FALA_ _Mundo_".split()

        def get_trans_minutia(u_name):
            data = self.banco.search(self.query.user == u_name)[0]["jogada"]

            def parse_carta(carta):
                return [carta] if "_" not in carta else carta.split("_")

            items = [(set(carta for d in data if d["ponto"] == game for carta in parse_carta(d["carta"])
                          ), game) for game in games]
            return items

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

    def build_User_table_for_prog(self, measure="delta", prog="prog", slicer=32, filename="/table.tab", learn=False):
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

    def build_User_table_as_timeseries(self, measure="delta", slicer=128, filename="/timeseries.tab", learn=False):
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

        :param measure: Um dos possiveis itens de medida do banco: tempo, delta, carta
        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :param learn: elimina linhas sem prognóstico
        :return:
        """

        def headed_data(dat, index):
            import pywt
            if not dat or len(dat) < slicer:
                return []
            print(len(dat))
            mode = pywt.MODES.sp1

            w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat[2:], w, mode)
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

    def normatize_for_isomorphic_classification(self, data):
        data_scale = 20.0 / max(float(max(data)) - float(min(data)), 1)
        data_floor = float(min(data))
        print(data_scale, data)
        data_isomorphism_lattice = "".join(str(int(((datum - data_floor) * data_scale) // 10))
                                           for datum in data).strip("0") or "000000"
        self.iso_classes.append(data_isomorphism_lattice)
        return data_isomorphism_lattice

    def build_interpolated_derivative_minutia_as_timeseries(
            self, slicer=16, filename="/interpolatedminutiatimeseries.tab", threshold=6):
        """
        Gera um arquivo tab do Orange para analise harmônica de minucias de segunda ordem interploadas no tempo.

        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :param threshold: elimina linhas sem prognóstico
        :return:
        """

        def headed_data(dat, index):
            import pywt
            if not dat or len(dat) < slicer:
                return []
            print(len(dat))
            mode = pywt.MODES.sp1

            w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat[2:], w, mode)
            print(wavelet)
            return ["%s%0d3" % (dat[0], index), "c", ""] + list(wavelet)
        span = slicer*8
        time, delta, game = self.resample_user_deltas_games()

        self.full_data = [(timer, float(turn) - float(turn0), user.prog, gamer, user.user)
                          for user in self.user
                          for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]
        data = [headed_data(self._encontra_minucia_interpolada(slicer=slicer, threshold=threshold), i)
                for i in range(span) if self.full_data]
        data = [line for line in data if line]
        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            w = writer(writecsv, delimiter='\t')
            data = zip(*data)
            for line in data:
                print(line)
                w.writerow(line)
            return data

    def build_interpolated_derivative_minutia(
            self, slicer=16, filename="/interpolatedminutia.tab", threshold=6):
        """
        Gera um arquivo tab do Orange para analise harmônica de minucias de segunda ordem interploadas no tempo.

        :param slicer: recorta eos dados neste tamanho
        :param filename: o nomo do aqrquivo que se quer gerar
        :param threshold: elimina linhas sem prognóstico
        :return:
        """

        def headed_data(dat, index):
            import pywt
            if not dat or len(dat) < slicer:
                return []
            print(len(dat))
            mode = pywt.MODES.sp1

            w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat[2:], w, mode)
            print(wavelet)
            return ["%s%0d3" % (dat[0], index), dat[1]] + list(wavelet)
        span = slicer*64
        time, delta, game = self.resample_user_deltas_games()

        self.full_data = [(timer, float(turn) - float(turn0), user.prog, gamer, user.user)
                          for user in self.user
                          for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]
        data = [headed_data(self._encontra_minucia_interpolada(slicer=slicer, threshold=threshold), i)
                for i in range(span) if self.full_data]
        data = [[name, self.normatize_for_isomorphic_classification(dat)] + dat for name, _, *dat in data if name]
        print(len(set(self.iso_classes)))

        with open(os.path.dirname(__file__) + filename, "wt") as writecsv:
            w = writer(writecsv, delimiter='\t')
            w.writerow(['n', 'CL'] + ['t%d' % t for t in range(slicer)])  # primeiro cabeçalho
            print('cabs', len(self.full_data), len((['n', 'CL'] + ['t%d' % t for t in range(32)])))

            w.writerow(['d'] + ['d' if t == 0 else 'c' for t in range(slicer+1)])
            w.writerow(['m'] + ['c' if t == 0 else '' for t in range(slicer+1)])
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
        data = [[user["user"], user[prog]] + [turn[measure] for turn in user["jogada"]][:slicer] for user in
                self.banco.all()]
        return data

    def train_classify_wnn(self, filename="/minucias.tab"):
        from enplicow import Wisard
        bleacher = dict(VM=0, SM=0, EM=0, FM=0, VC=0, SC=0, EC=0, FC=0, VF=0, SF=0, EF=0, FF=0)
        # print(v, s, f, e, b, a, d, DATA[0])
        data = self.read_csv_data(filename)
        endtime = 34
        print(data[0])
        data = [(line[0], line[1][-1] + line[1][1],
                 Wisard.retinify([float(t) + 10 for t in line[3:endtime]]))
                for line in data]

        w = Wisard(data, 32 * 32, bleach=800000, mapper=bleacher, enf=100, sup=10)
        confidence = w.single(print_result=True, namer=-2)
        print(confidence, 100 - confidence)
        return 100 - confidence

    def read_csv_data(self, filename):
        import csv
        with open(os.path.dirname(__file__) + filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            self.data = [row for row in spamreader][3:]
        return self.data

    def plot_derivative_minutia(self, filename="/minucias.tab"):
        import matplotlib.pyplot as plt
        from math import pi
        from enplicow import COLORS
        max_len = 32
        data = self.read_csv_data(filename)
        clazzes = list(set([clazz for _, clazz, *_ in data]))
        clazzes.sort()
        data = {clazz: [cdata + [0.0]*(max_len - len(cdata))
                        for _, aclazz, *cdata in data if aclazz == clazz][:8] for clazz in clazzes}
        step = 2 * pi / 32
        theta = [ang * step for ang in range(32)]

        fig = plt.figure(figsize=(9, 9))
        fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
        for n, title in enumerate(clazzes):
            case_data = data[title]
            ax = fig.add_subplot(3, 4, n + 1, projection='polar')
            # plt.rgrids([0.2, 0.4, 0.6, 0.8])
            ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                         horizontalalignment='center', verticalalignment='center')
            for color, line in zip(COLORS, case_data):
                line = [float(dot) + 7.0 for dot in line]
                print(len(theta), len(line))
                ax.plot(theta, line, color=color, linewidth=2)

            ax.set_rmax(15.0)
            ax.grid(True)
        # add legend relative to top-left plot
        # plt.subplot(2, 2, 1)
        # labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
        # legend = plt.legend(labels, loc=(0.9, .95), labelspacing=0.1)
        # plt.setp(legend.get_texts(), fontsize='small')

        plt.figtext(0.5, 0.965, 'Classes de minucias segundo  jogo x transitividade',
                    ha='center', color='black', weight='bold', size='large')
        plt.show()


if __name__ == '__main__':
    # Learn().report_user_data()
    # Learn().report_user_turn()
    # Learn().build_User_table_for_prog(slicer=128, learn=False, filename="/fullderivative.tab")
    # Learn().build_user_table_for_minucia(slicer=128, filename="/fullminucias.tab", learn=False)
    # Learn().build_user_table_for_minucia(slicer=1024, threshold=16, filename="/largeminucias.tab", learn=True)
    # Learn().train_classify_wnn()
    # Learn().plot_derivative_minutia()
    # Learn().build_User_table_as_timeseries()
    # Learn().build_derivative_minutia_as_timeseries(filename="/minutia16timeseries.tab")
    Learn().load_from_db().build_interpolated_derivative_minutia(slicer=4, threshold=3)
    # Learn().load_from_db().build_interpolated_derivative_minutia_as_timeseries(slicer=12, threshold=8)
    #Learn().load_from_db().resample_user_deltas()
