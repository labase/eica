# -*- coding: UTF8 -*-
# import operator
import os
from csv import writer

import matplotlib.pyplot as plt
import pywt
from tinydb import TinyDB, Query
from matplotlib import collections as mc
import numpy as np

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
GAME_INDEX = dict(_Mundo_=2, _Chaves_=1, _FALA_=3, __A_T_I_V_A__=4,
                  _MUNDO_=2, _HOMEM_=2, _ABAS_=1, _CHAVES_=1, _LINGUA_=3)
PROG_INDEX = {key: value for value, key in enumerate("VSFE")}
CLAZ_INDEX = {key: value+4 for value, key in enumerate("VSFE")}
INDEX_GAME = {key + 1: value for key, value in enumerate("_Chaves_ _Mundo_ _FALA_ __A_T_I_V_A__".split())}
WAVELET_MODE = pywt.MODES.sp1
MACHINE_ORDER = [0, 2, 3, 1, 5, 4, 6, 7]
NUS = 50


class User:
    iso_classifier = {}

    def __init__(self, user, sexo, idade, ano, hora, nota, prog, trans, jogada):
        self.user, self.sexo, self.idade, self.ano, self.hora, self.nota, self.prog, self.trans, self.jogada = \
            user, sexo, idade, ano, hora, nota, prog, trans, []
        self.load_from_db(jogadas=jogada)
        # time, delta, game = self.resample_user_deltas_games()
        # self.janela_jogadas = [(timer, float(turn) - float(turn0), user.prog, gamer, user.user)
        #                   for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]
        self.iso_classifier = {}
        self.timed_minutia_buckets = [0] * 300
        self.labeled_minutia_events = []
        self.minutia_buckets = [0] * 40
        self.progclazz_minutia_buckets = [[0 for _ in range(40)] for _ in range(4 * 3)]
        self.janela_jogadas = []

    def write(self, db):
        attrs = "user, sexo, idade, ano, hora, nota, prog, trans, jogada".split(", ")
        db.insert({k: self.__dict__[k] if k != "jogada" else [jogada.read() for jogada in self.__dict__[k]]
                   for k in dir(self) if k in attrs})

    def load_from_db(self, jogadas):
        self.jogada = [Jogada(**user_data) for user_data in jogadas if "0" not in user_data]
        return self

    def interpolate_objects(self, delta=0.5):
        from scipy.interpolate import interp1d  # , splev, splrep, UnivariateSpline
        import numpy as np
        interpolate_objects = [(jogo.tempo, jogo.carta) for jogo in self.jogada][1:100]
        x, y, = zip(*interpolate_objects)
        interpolating_function = interp1d(x, y, kind='nearest')
        linear_time_space = np.linspace(x[0], x[-1], (x[-1] - x[0]) / delta)

        return linear_time_space, interpolating_function(linear_time_space)

    def interpolate_deltas(self, delta=0.5):
        from scipy.interpolate import interp1d  # , splev, splrep, UnivariateSpline
        import numpy as np
        interpolate_deltas = [(jogo.tempo, jogo.delta) for jogo in self.jogada][1:1000]
        x, y = zip(*interpolate_deltas)
        interpolating_function = interp1d(x, y)
        linear_time_space = np.linspace(x[0], x[-1], (x[-1] - x[0]) / delta)

        return linear_time_space, interpolating_function(linear_time_space)

    def interpolate_games(self, delta=1):
        from scipy.interpolate import interp1d
        import numpy as np
        interpolate_deltas = [(jogo.tempo, jogo.ponto) for jogo in self.jogada][1:]
        x, jogo = zip(*interpolate_deltas)
        y = self.combine_matching_games_into_indexed_sequence(jogo)
        interpolating_function = interp1d(x, y, kind='nearest')
        linear_time_space = np.linspace(x[0], x[-1], (x[-1] - x[0]) / delta)

        return linear_time_space, interpolating_function(linear_time_space)

    @staticmethod
    def combine_matching_games_into_indexed_sequence(jogo):
        print(jogo[0])
        # jogo = ['_'] + jogo + ['_']
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
        return y

    def interpolate_card_cross_usage(self, delta=1):
        from scipy.interpolate import interp1d
        import numpy as np
        str_index = {}
        index_str = {}
        total_card = [set(), set(), set(), set()]

        def parse_carta(carta):
            carta = index_str[int(carta)]
            # print("parse_carta", carta)
            return [get_str_index(int(carta))] if carta.isdigit() else [] if "__" in carta \
                else [int(ct) - 1 for ct in carta.split("_") if ct] if "mini" not in carta else []

        def get_str_index(token):
            index = len(str_index)
            if token not in str_index:
                str_index[token] = index
                index_str[index] = token
            return index

        def iterate(jogada):
            blacklist = "minitens fruta animal objeto __A_T_I_V_A__".split()
            for jogo in jogada:
                tempo, carta, ponto = jogo.tempo, jogo.carta, jogo.ponto
                # if "A" in carta: print(carta)
                carta = [int(carta)] if carta.isdigit() else [int(ct) for ct in carta.split("_")
                                                              if ct] if carta not in blacklist else []
                if carta:
                    for delta_tempo, uma_carta in enumerate(carta):
                        yield tempo + delta_tempo * 0.2, uma_carta, GAME_INDEX[ponto]-1
                else:
                    continue

        interpolate_cards = [(tempo, carta, ponto) for tempo, carta, ponto in iterate(self.jogada[1:])]
        print(interpolate_cards)
        if not interpolate_cards:
            return [], []
        # interpolate_cards = [(jogo.tempo, get_str_index(jogo.carta)) for jogo in self.jogada][1:]
        x, card, game = zip(*interpolate_cards)
        interpolating_card = interp1d(x, card, kind='nearest')
        # game = self.combine_matching_games_into_indexed_sequence(tuple(jogo.ponto for jogo in self.jogada)[1:])
        interpolating_game = interp1d(x, game, kind='nearest')
        linear_time_space = np.linspace(x[0], x[-1], (x[-1] - x[0]) / delta)

        def update_game_usage_sets(crd, gme):
            total_card[int(gme)].add(int(crd))
            # return (len(total_card[0] | total_card[1] | total_card[2]), len(total_card[0]), len(total_card[1]),
            #         len(total_card[2]),
            #         len(total_card[0] & total_card[1] & total_card[2]))
            return (len(total_card[0] | total_card[1] | total_card[2]), len(total_card[0] & total_card[1]),
                    len(total_card[1] & total_card[2]), len(total_card[0] & total_card[2]),
                    len(total_card[0] & total_card[1] & total_card[2]))

        cross_usage = [update_game_usage_sets(crd, gme)
                       for crd, gme in
                       zip(interpolating_card(linear_time_space), interpolating_game(linear_time_space))]
        print("total_card,", total_card)
        print("cross_usage,", cross_usage)

        return linear_time_space, cross_usage

    def resample_user_deltas_games(self, span=200000):
        _, delta = self.interpolate_deltas()
        time, game = self.interpolate_games()
        self.janela_jogadas = [(timer, float(turn) - float(turn0), self.prog, gamer, self.user)
                               for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]
        return self.janela_jogadas

    def encontra_minucias_interpolada_em_jogo(self, threshold=8):
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

    @staticmethod
    def classify_by_normatized_isomorphism(data):
        # print("classify_by_normatized_isomorphism", data)
        data = data[:3]
        span = (float(max(data)) - float(min(data)))
        data_scale = 29.0 / span if span else 1
        data_floor = float(min(data))
        # print("classify_by_normatized_isomorphism", data_scale, data, self.user)
        data_isomorphism_lattice = "".join(str(int(((datum - data_floor) * data_scale) // 10))
                                           for datum in data).strip("0") or "0"
        if data_isomorphism_lattice not in User.iso_classifier:
            User.iso_classifier[data_isomorphism_lattice] = data_isomorphism_lattice
        return (data_isomorphism_lattice in User.iso_classifier) and User.iso_classifier[data_isomorphism_lattice]

    def old_scan_resampled_minutia(self, isoclazz, slicer, isoclazz_minutia_buckets, compute_timed_minutia):
        def headed_data(dat):
            import pywt
            if not dat or len(dat) < slicer:
                return []
            mode = pywt.MODES.sp1

            w = pywt.Wavelet('db3')
            # w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat, w, mode)
            # print("wavelet", len(dat), wavelet)
            return list(wavelet)

        while self.janela_jogadas:
            time_slice = self.encontra_minucias_interpolada_em_jogo()
            if not time_slice:
                break
            tempo, data, clazzes, jogo, user = list(zip(*time_slice))
            slicer = 4
            while len(data) >= slicer:
                # print("time_slice", data[:slicer])
                clazz = self.classify_by_normatized_isomorphism(headed_data(data[:slicer]))
                if clazz not in isoclazz:
                    isoclazz.append(clazz)
                if tempo[0] < 300:
                    compute_timed_minutia(clazz, isoclazz, tempo)
                if clazz not in isoclazz_minutia_buckets:
                    isoclazz_minutia_buckets[clazz] = 0
                else:
                    isoclazz_minutia_buckets[clazz] += 1
                if clazzes[0]:
                    # print("progclazz_minutia_buckets", clazzes[0], isoclazz.index(clazz), jogo[0])
                    self.progclazz_minutia_buckets[3 * PROG_INDEX[clazzes[0]] + int(jogo[0]) - 1][
                        isoclazz.index(clazz)] += 1
                slicer = 3
                data = data[slicer:]
                clazzes = clazzes[slicer:]
                jogo = jogo[slicer:]
                user = user[slicer:]

    def scan_resampled_minutia(self, isoclazz, _, isoclazz_minutia_buckets, compute_timed_minutia):
        def headed_data(dat):
            import pywt
            mode = pywt.MODES.sp1

            w = pywt.Wavelet('db3')
            # w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(dat, w, mode)
            # print("wavelet", len(dat), wavelet)
            return list(wavelet)

        for time_slice in zip(*(iter(self.janela_jogadas),) * 4):
            if len(time_slice) < 3:
                break
            tempo, data, clazzes, jogo, user = list(zip(*time_slice))
            # print("time_slice", data[:slicer])
            clazz = self.classify_by_normatized_isomorphism(headed_data(data))
            if clazz not in isoclazz:
                isoclazz.append(clazz)
            if tempo[0] < 300:
                compute_timed_minutia(clazz, isoclazz, tempo)
            if clazz not in isoclazz_minutia_buckets:
                isoclazz_minutia_buckets[clazz] = 0
            else:
                isoclazz_minutia_buckets[clazz] += 1
            if clazzes[0]:
                # print("progclazz_minutia_buckets", clazzes[0], isoclazz.index(clazz), jogo[0])
                self.progclazz_minutia_buckets[3 * PROG_INDEX[clazzes[0]] + int(jogo[0]) - 1][
                    isoclazz.index(clazz)] += 1

    def compute_minutia_count(self, clazz, isoclazz, tempo):
        """
        Soma as ocorrências de minúcias em um intervalode 10 segundos.

        :param clazz: classe identificadora da minucia
        :param isoclazz: lista para converter a classe identificadora em um índice inteiro
        :param tempo: selo de tempo onde a minúcia ocorre
        :return:
        """
        self.timed_minutia_buckets[int(tempo[0]) // 10] += (isoclazz.index(clazz) + 1)
        self.minutia_buckets[isoclazz.index(clazz)] += 1

    def track_minutia_event(self, clazz, isoclazz, tempo):
        """
        Rastreia a ocorrência de minúcias e armazena os tempos de seus eventos.

        :param clazz: classe identificadora da minucia
        :param isoclazz: lista para converter a classe identificadora em um índice inteiro
        :param tempo: selo de tempo onde a minúcia ocorre
        :return:
        """
        self.minutia_buckets[isoclazz.index(clazz)].append(int(tempo[0]))
        self.labeled_minutia_events.append(isoclazz.index(clazz))


class Jogada:
    def __init__(self, tempo, delta, ponto, carta, casa, valor, move):
        self.tempo, self.delta, self.ponto, self.carta, self.casa, self.valor, self.move = \
            tempo, delta, ponto, carta, casa, valor, move

    def read(self):
        attrs = "tempo, delta, ponto, carta, casa, valor, move".split(", ")
        return {k: self.__dict__[k] for k in dir(self) if k in attrs}

    def update(self, **kwargs):
        attrs = "tempo, delta, ponto, carta, casa, valor, move".split(", ")
        [setattr(self, attr, value) for attr, value in kwargs.items() if attr in attrs]
        return self


class Estado:
    STATE_DIGEST = {}
    STATE_INVENTORY = {}
    STATE_INDEX = []
    INDEX_STATE = {}

    def __init__(self, tipo, tempo):
        """
        Estado é um estágio de processamento da máquina EICA.

        :param tipo: Tipo do estado no máquina EICA
        :param tempo: Evento de ocorrência do estado
        """
        self.tempo, self.tipo = tempo, tipo
        self.profile = set()
        self.machine_count = {key: 0 for key in CARDS}
        self.user_count = {}
        self.user_latency = []
        self.user_duration = []
        self.user_interval = []

    @staticmethod
    def wavelet(dat, slicer=4):
        if not dat or len(dat) < slicer:
            return []
        dat = dat[:4]
        data_span = (float(max(dat)) - float(min(dat)))
        data_scale = 1000.0 / data_span if data_span else 1
        data_floor = float(min(dat))
        scaled_data = [int(((datum - data_floor) * data_scale) // 10) for datum in dat]

        w = pywt.Wavelet('bior1.5')
        # w = pywt.Wavelet('sym5')
        _, wavelet = pywt.dwt(scaled_data, w, WAVELET_MODE)
        # print("fan in wavelet", len(scaled_data), wavelet)
        wavelet_profile = list(wavelet)
        return wavelet_profile

    @staticmethod
    def identify(dat, slicer=4):
        wavelet_profile = Estado.wavelet(dat, slicer=slicer)[:3]
        span = (float(max(wavelet_profile)) - float(min(wavelet_profile)))
        data_scale = 27.0 / span if span else 1
        data_floor = float(min(wavelet_profile))
        # print("classify_by_normatized_isomorphism", data_scale, wavelet_profile)
        data_isomorphism_lattice = "".join(str(int(((datum - data_floor) * data_scale) // 10))
                                           for datum in wavelet_profile).strip("0") or "0"
        if data_isomorphism_lattice not in Estado.STATE_DIGEST:
            Estado.STATE_DIGEST[data_isomorphism_lattice] = data_isomorphism_lattice
        return (data_isomorphism_lattice in Estado.STATE_DIGEST) and Estado.STATE_DIGEST[data_isomorphism_lattice]

    def update(self, jogo, user, data):
        # self.machine_count[jogo] += 1
        self.profile.add(data)
        if user[0] not in self.user_count:
            self.user_count[user[0]] = 1
        else:
            self.user_count[user[0]] += 1

    @staticmethod
    def scan_data_for_minutia(janela_jogadas):
        isoclazz = Estado.STATE_INDEX
        stated_marked_time_series = []

        for time_slice in zip(*(iter(janela_jogadas),) * 4):
            if len(time_slice) < 3:
                break
            tempo, data, clazzes, jogo, user = list(zip(*time_slice))
            # print("time_slice", data[:slicer])
            # data = tuple(Estado.wavelet(data))
            data_span = (float(max(data)) - float(min(data)))
            data_scale = 30.0 / data_span if data_span else 1
            data_floor = float(min(data))
            scaled_data = tuple(int(((datum - data_floor) * data_scale) // 10) for datum in data)
            # data = scaled_data
            # scaled_data = tuple(Estado.wavelet(data))
            # print("scan_data_for_minutia", scaled_data)
            clazz = Estado.identify(data)
            if clazz not in isoclazz:
                isoclazz.append(clazz)
                Estado.INDEX_STATE[clazz] = len(isoclazz)
                Estado.STATE_INVENTORY[Estado.INDEX_STATE[clazz]] = estado = Estado(clazz, 0)
                estado.update(jogo, user, data)
            else:
                Estado.STATE_INVENTORY[Estado.INDEX_STATE[clazz]].update(jogo, user, data)
            stated_marked_time_series += [(Estado.INDEX_STATE[clazz], *full_state)
                                          for full_state in zip(tempo, data, clazzes, jogo, user)]
        return stated_marked_time_series

    def register_profile(self, wave):
        self.profile.append(wave)


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
        self.state_burst = {}
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
            dat = dat[:4]
            mode = pywt.MODES.sp1
            data_span = (float(max(dat)) - float(min(dat)))
            data_scale = 1000.0 / data_span if data_span else 1
            data_floor = float(min(dat))
            scaled_data = [int(((datum - data_floor) * data_scale) // 10) for datum in dat]

            w = pywt.Wavelet('bior1.5')
            # w = pywt.Wavelet('sym5')
            _, wavelet = pywt.dwt(scaled_data, w, mode)
            # print("fan in wavelet", len(scaled_data), wavelet)
            return list(wavelet)

        time, delta, game = self.resample_user_deltas_games()
        user_index = {user.user: index for index, user in enumerate(self.user)}
        self.user_timed_minutia_buckets = [[0 for _ in range(300)] for _ in range(NUS)]
        self.user_minutia_buckets = [[0 for _ in range(40)] for _ in range(70)]
        self.progclazz_minutia_buckets = [[0 for _ in range(40)] for _ in range(4 * 3)]
        self.isoclazz_minutia_buckets = {i_clazz: 0 for i_clazz in set(self.iso_classes)}
        User.iso_classifier = {clazz: clazz for clazz in set(self.iso_classes)}

        self.full_data = [(timer, float(turn) - float(turn0), user.prog, gamer, user.user)
                          for user in self.user
                          for timer, turn, turn0, gamer in zip(time, delta[1:span], delta[:span], game)]
        print("len(self.full_data)", len(self.full_data), self.full_data[0], User.iso_classifier)
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
                    self.user_timed_minutia_buckets[user_index[user[0]]][int(tempo[0]) // 10] += isoclazz.index(clazz)
                    self.user_minutia_buckets[user_index[user[0]]][isoclazz.index(clazz)] += 1
                if clazz not in self.isoclazz_minutia_buckets:
                    self.isoclazz_minutia_buckets[clazz] = 0
                else:
                    self.isoclazz_minutia_buckets[clazz] += 1
                if clazzes[0]:
                    print("progclazz_minutia_buckets", clazzes[0], isoclazz.index(clazz), jogo[0])
                    self.progclazz_minutia_buckets[3 * PROG_INDEX[clazzes[0]] + int(jogo[0]) - 1][
                        isoclazz.index(clazz)] += 1
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
        print(sum(count for user in self.user_minutia_buckets for count in user))
        print(sum(1 for user in self.user_minutia_buckets if any(user)))
        self.plot_derivative_minutia_by_user_prognostics_games()
        return
        # plt.imshow(zi, vmin=min(z), vmax=max(z), origin='lower',
        #            extent=[min(x), max(x), min(y), max(y)])
        # plt.scatter(x, y, c=z)
        # plt.colorbar()
        # plt.show()

    def scan_for_minutia_count_in_user_and_games(
            self, slicer=16):
        """
        Rastreia a série temporal de cada usuário para identificar as minúcias derivativas.

        :param slicer: recorta eos dados neste tamanho
        :return:
        """
        self.user_timed_minutia_buckets = [[0 for _ in range(300)] for _ in range(NUS)]
        self.user_minutia_buckets = [[0 for _ in range(40)] for _ in range(70)]
        self.progclazz_minutia_buckets = [[0 for _ in range(40)] for _ in range(4 * 3)]
        self.isoclazz_minutia_buckets = {i_clazz: 0 for i_clazz in set(self.iso_classes)}
        User.iso_classifier = {clazz: clazz for clazz in set(self.iso_classes)}
        isoclazz = []
        for user in self.user:
            if len(user.jogada) < 4:
                continue
            user.resample_user_deltas_games()
            user.scan_resampled_minutia(isoclazz, slicer, self.isoclazz_minutia_buckets, user.compute_minutia_count)
        print("isoclazz_minutia_buckets", len(self.isoclazz_minutia_buckets), self.isoclazz_minutia_buckets)
        print("iso_classes", {oc: sum(1 for c in self.iso_classes if c == oc) for oc in set(self.iso_classes)})
        print("progclazz_minutia_buckets", self.progclazz_minutia_buckets)
        print("iso_classifier", User.iso_classifier)
        print("user", [u.user for u in self.user[:NUS]])
        print("user_minutia_buckets", self.user_minutia_buckets)
        for user in self.user:
            print(user.user, user.minutia_buckets)
        # self.plot_derivative_minutia_by_prognostics_games()
        print("countuser_minutia_buckets", sum(count for user in self.user for count in user.minutia_buckets))
        print("sumuser_minutia_buckets", sum(1 for user in self.user if any(user.minutia_buckets)))
        # self.plot_derivative_minutia_by_user()
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
        # print("classify_by_normatized_isomorphism", data_scale, data)
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
        end = min(slicer - 1, min(
            i if a == ojogo != b else 2 ** 100 for i, a, b in zip(tempo, jogo[:slicer], jogo[1:slicer]))) + 1
        # print(len(self.full_data), ojogo, start, end, [umaclazz for umaclazz in CARDS])
        self.full_data = self.full_data[end:]
        ojogo = INDEX_GAME[ojogo]
        clazz = "_%s_%s_" % (ojogo[1], clazzes[start]) if clazzes[start] else "_%s_._" % ojogo[1]
        if (end - start) < threshold:
            return []
        return [sigla(user[start], clazz), clazz] + list(derivada[:end]) + [0.0] * (slicer - end)

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

    def plot_derivative_minutia_by_user(self):
        import numpy as np
        import matplotlib.pyplot as plt
        import scipy.interpolate
        from mpl_toolkits.mplot3d import Axes3D
        assert Axes3D
        from matplotlib import cm
        # Generate data:
        x, y, z = zip(*[(x, y, user.timed_minutia_buckets[y])
                        for y in range(300) for x, user in enumerate(self.user[:NUS])])
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
        ax.set_zlim(0, 300)
        # labels = "v.s. chaves,v.s. mundo,v.s. fala,s.m. chaves,s.m. mundo,s.m. fala," \
        #          "f.s. chaves,f.s. mundo,f.s. fala,e.s. chaves,e.s. mundo,e.s. fala,".split(",")
        # ax.plot_trisurf(x, y, zi, cmap=cm.jet, linewidth=0.2)
        # plt.xticks(x, labels, rotation='vertical')
        ax.plot_surface(xi[::-1], yi, zi, rstride=1, cstride=1, color='b', cmap=cm.coolwarm,
                        linewidth=0, antialiased=False, shade=False)
        plt.show()

    def scan_states_in_full_data_plus_user(self):
        for user in self.user:
            if len(user.jogada) < 4:
                continue
            user.minutia_buckets = {minutia_id: [] for minutia_id in range(40)}
            resampled_data = user.resample_user_deltas_games()
            yield Estado.scan_data_for_minutia(resampled_data), user

    def scan_states_in_full_data(self):
        for user in self.user:
            if len(user.jogada) < 4:
                continue
            user.minutia_buckets = {minutia_id: [] for minutia_id in range(40)}
            resampled_data = user.resample_user_deltas_games()
            yield Estado.scan_data_for_minutia(resampled_data)


class MinutiaProfiler(Track):
    """
    Levanta os perfis de onda para cada estado EICA
    """

    def collect_state_burst_information(self, named_user=None):
        # user_data = [user for user in self.scan_states_in_full_data()]
        for user_data, user_object in self.scan_states_in_full_data_plus_user():
            # print(user_data[0][-1])
            if named_user and named_user != user_data[0][-1]:
                continue
            # states, time, data, _, _, user = zip(*user_data)
            user_collected_burst = "0"
            for state, time, data, claz, jogo, user in user_data:
                # print("state, time, data, _, _, user", state, time, data, user)

                if state == 1:
                    if user_collected_burst != "0":
                        if user_collected_burst in self.state_burst:
                            ucb = self.state_burst[user_collected_burst]
                            ucb[0] += 1
                            ucb[int(jogo)] += 1
                            if claz:
                                ucb[CLAZ_INDEX[claz]] += 5
                        else:
                            self.state_burst[user_collected_burst] = ucb = [1, 0, 0, 0, 0, 0, 0, 0]
                            ucb[int(jogo)] += 1
                            if claz:
                                ucb[CLAZ_INDEX[claz]] += 5
                        user_collected_burst = "0"
                else:
                    user_collected_burst += "" if str(state-1) == user_collected_burst[-1] else str(state-1)
        best_burst = [(g, k, c, m, r, v, f, s, e) for k, (g, c, m, r, v, f, s, e) in self.state_burst.items() if v>1]
        best_burst.sort()
        gcount, labels, c, m, r, v, f, s, e = zip(*best_burst)
        self.plot_burst_usage_and_size([labels, gcount, c, m, r, v, f, s, e])
        print("collect_state_burst_information", len(self.state_burst), len(best_burst), best_burst )

    def survey_orc_transitivity_in_time(self, named_user=None):
        # user_data = [user for user in self.scan_states_in_full_data()]
        for user_data, user_object in self.scan_states_in_full_data_plus_user():
            # print(user_data[0][-1])
            if named_user and named_user != user_data[0][-1]:
                continue
            cross_orc_usage = user_object.interpolate_card_cross_usage()
            # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
            if cross_orc_usage[0] == []:
                continue
            # data_collection, state_collection, user = self.create_state_colored_derivative_data(
            #     user_data)
            data_collection, state_collection, user = self.create_interpolated_state_colored_derivative_data(
                user_data, cross_orc_usage[0])
            self.plot_state_colored_segments(user_object.user, data_collection, state_collection, cross_orc_usage)
            # self.plot_state_colored_segments("nono", lines, [1, 2, 3], cross_orc_usage)
            pass

    def cross_usage_in_user(self, u_name):
        data = self.list_user_data(u_name)
        games = "_Chaves_ _FALA_ _Mundo_".split()

        def parse_carta(carta):
            return [carta] if "_" not in carta else carta.split("_")

        items = [set(carta for d in data if d["ponto"] == game for carta in parse_carta(d["carta"])
                     ) for game in games]
        return u_name, len(items[0] | items[1] | items[2]), len(items[0] & items[1]), len(items[1] & items[2]), \
               len(items[0] & items[2]), len(items[0] & items[1] & items[2])

    def plot_item_use_across_games(self):
        u_names = list(set(self.new_find_all_users_names()))
        udata = [self.cross_usage_in_user(u_name) for u_name in u_names]
        udata.sort(key=lambda u: sum(u[1:]))
        ubars = list(zip(*udata))
        labels = ubars.pop(0)
        labels = [
            " ".join([part.capitalize() if i == 0 else part[:1].capitalize() for i, part in enumerate(name.split())])
            for name in labels]
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
        plt.bar(x, ubars[2], bottom=[i + j for i, j in zip(ubars[0], ubars[1])], color="b", label=legend[2],
                linewidth=0)
        plt.bar(x, ubars[3], bottom=[i + j + k for i, j, k in
                                     zip(ubars[0], ubars[1], ubars[2])], color="m", label=legend[3], linewidth=0)
        plt.bar(
            x, ubars[4], bottom=[i + j + k + l for i, j, k, l in
                                 zip(ubars[0], ubars[1], ubars[2], ubars[3])], color="c", label=legend[4], linewidth=0)
        plt.legend(ncol=2, loc="upper left")
        plt.show()
        return

    def plot_burst_usage_and_size(self, ubars):
        labels = ubars.pop(0)
        labels = [
            " ".join([part.capitalize() if i == 0 else part[:1].capitalize() for i, part in enumerate(name.split())])
            for name in labels]
        legend = "Contagem global,Contagem no Chaves,Contagem no Mundo,Contagem no Fala," \
                 "Contagem Verdadeiros,Contagem Sucesso,Contagem Falso,Contagem Expulsão".split(",")
        print(legend)
        # cl = "r g b c m y".split()
        plt.grid(True)
        plt.subplots_adjust(bottom=0.5, left=.05, right=.96, top=0.96, hspace=.35)
        plt.title("Contagem dos casos de uso da máquina EICA")

        x = range(len(ubars[0]))
        plt.xticks(x, labels, rotation='vertical')
        # for i, bar in enumerate(ubars):
        #     plt.bar(x, bar, bottom=None if i == 0 else ubars[i-1], color=cl[i])
        print(ubars[:10])
        plt.bar(x, ubars[0], color="r", label=legend[0], linewidth=0, log=1)

        plt.bar(x, ubars[1], bottom=ubars[0], color="g", label=legend[1], linewidth=0)
        plt.bar(x, ubars[2], bottom=[i + j for i, j in zip(ubars[0], ubars[1])], color="b", label=legend[2],
                linewidth=0)
        plt.bar(x, ubars[3], bottom=[i + j + k for i, j, k in
                                     zip(ubars[0], ubars[1], ubars[2])], color="m", label=legend[3], linewidth=0)
        plt.bar(
            x, ubars[4], bottom=[i + j + k + l for i, j, k, l in
                                 zip(ubars[0], ubars[1], ubars[2], ubars[3])], color="c", label=legend[4], linewidth=0)
        plt.bar(
            x, ubars[5], bottom=[i + j + k + l + m for i, j, k, l, m in
                                 zip(ubars[0], ubars[1], ubars[2], ubars[3], ubars[4])], color="y", label=legend[5], linewidth=0)
        plt.bar(
            x, ubars[6], bottom=[i + j + k + l + m + n for i, j, k, l, m, n in
                                 zip(ubars[0], ubars[1], ubars[2], ubars[3], ubars[4], ubars[5])], color="k", label=legend[6], linewidth=0)
        plt.bar(
            x, ubars[7], bottom=[i + j + k + l + m + n + o for i, j, k, l, m, n, o in
                                 zip(ubars[0], ubars[1], ubars[2], ubars[3], ubars[4], ubars[5], ubars[6])], color="pink", label=legend[7], linewidth=0)
        """        """

        plt.legend(ncol=2, loc="upper left")
        plt.show()
        return

    def plot_derivative_marked_states(self):
        user_data = [user for user in self.scan_states_in_full_data()]
        for user in user_data:
            self.plot_user_states(user)

    def plot_user_states(self, user_data):
        data_collection, state_collection, user = self.create_state_colored_derivative_data(user_data)
        self.plot_state_colored_segments(user[0], data_collection, state_collection)

    def create_interpolated_state_colored_derivative_data(self, user_data, interpolating_time):
        from scipy.interpolate import interp1d  # , splev, splrep, UnivariateSpline
        states, time, data, _, _, user = zip(*user_data)
        data = [(x, y1 - y0) for x, y0, y1 in zip(time, data, data[1:])]
        interpolating_function = interp1d(*zip(*data))
        # data = [(x, y1 - y0) for x, y0, y1 in zip(range(len(data)), data, data[1:])]
        # data = [(x, y1-y0) for x, y0, y1 in zip(time, data, data[1:])]
        # data = [(x, y) for x, y in zip(range(len(data)), data)]
        while interpolating_time[-1] > time[-1]:
            interpolating_time = interpolating_time[:-3]
            print(interpolating_time[-3], time[-1])
        data = [(y, float(interpolating_function(y))) for y in interpolating_time[1:-2]]
        interpolating_function = interp1d(time, states)
        states = [interpolating_function(y) for y in interpolating_time]
        data_collection = list(zip(*(iter(data),) * 4))
        data_collection = [segment + (complement[0],) for segment, complement in
                           zip(data_collection, data_collection[1:])]
        state_collection = [st[0] for st in zip(*(iter(states),) * 4)]
        return data_collection, state_collection, user

    def create_state_colored_derivative_data(self, user_data):
        states, time, data, _, _, user = zip(*user_data)
        data = [(x, y1 - y0) for x, y0, y1 in zip(time, data, data[1:])]
        # data = [(x, y1 - y0) for x, y0, y1 in zip(range(len(data)), data, data[1:])]
        # data = [(x, y1-y0) for x, y0, y1 in zip(time, data, data[1:])]
        # data = [(x, y) for x, y in zip(range(len(data)), data)]
        data_collection = list(zip(*(iter(data),) * 4))
        data_collection = [segment + (complement[0],) for segment, complement in
                           zip(data_collection, data_collection[1:])]
        state_collection = [st[0] for st in zip(*(iter(states),) * 4)]
        return data_collection, state_collection, user

    def profile_wave_case_for_all_events(self):
        _ = [user for user in self.scan_states_in_full_data()]
        data = [[]] * 8
        print(Estado.STATE_INVENTORY)
        for index, estado in Estado.STATE_INVENTORY.items():
            print(index, len(estado.profile))
            data.insert(MACHINE_ORDER.index(index - 1), estado.profile)
        labels = ["estado %d" % i for i in range(8)]
        data = [[[float(y) + i / 150 for y in plot] for i, plot in enumerate(st)] for st in data]
        return
        self.boxplot_de_caracteristicas(data, labels, complemento=": perfil de ondas")

    @staticmethod
    def boxplot_de_caracteristicas(data, labels, complemento=" individual", filename=None):
        import matplotlib.pyplot as plt
        # labels = 'Contagem de estados,Latência de estados,Intervalo entre estados,Permanência no estado'.split(",")
        profile = data[:]
        fig, axes = plt.subplots(nrows=len(labels) // 2, ncols=2, figsize=(8, 12))
        # fig.tight_layout()
        for axc in axes:
            # plt.subplot(311+prop)
            # ax = ax.flatten()
            for ax in axc:
                waveprof = profile.pop(0)
                for wave in waveprof:
                    ax.plot(wave)
                ax.yaxis.grid(True)
                # ax.set_xticks([y + 1 for y in range(len(data))])
                ax.set_xlabel('Tempo em segundos')
                ax.set_title(labels.pop(0) + complemento)
                ax.set_ylabel("aceleração")
                ax.set_ylim(ymin=0)
        # plt.ylim(ymin=0)
        plt.subplots_adjust(hspace=0.5)
        if filename:
            plt.savefig(filename + ".png")
        else:
            plt.show()

    @staticmethod
    def plot_state_colored_segments(u_name, derivative_data, state_coloring, cross_game_data=None):
        # color = ["ff0000", "00ff00", "0000ff", "orange", "magenta", "cyan", "black", 'yellow', 'red']
        color = ['red', 'green', 'blue', "orange", "magenta", "cyan", "black", 'yellow', 'red']
        legend = "Objetos usados,Trans chave/fala,Trans fala/mundo,Trans chave/mundo,Trans total".split(",")
        colored_states = [color[int(state)] for state in state_coloring]
        print(derivative_data[:3])
        lc = mc.LineCollection(derivative_data, colors=colored_states, linewidths=2)
        fig1, ax = plt.subplots(figsize=(18, 12))
        # ax.set_ylim(-1, 1)        # ax.ylim(-5, 5)
        ax.set_ylim(-1, 60)        # ax.ylim(-5, 5)
        ax.set_xlabel('jogadas')
        ax.set_title(u_name)
        # ax.autoscale()
        x, y = cross_game_data
        ax.set_xlim(0, min(500, x[-1]))
        # print("xn, yn: ", len(x), len(y), len(list(zip(*y))), list(zip(*y)))
        y = np.row_stack(zip(*y))
        # y = np.row_stack(y)
        # print("xn, yn: ", len(x), len(y))
        # this call to 'cumsum' (cumulative sum), passing in your y data,
        # is necessary to avoid having to manually order the datasets
        y_stack = np.cumsum(y, axis=0)  # a 3x10 array
        # print("y_stack", len(y_stack[0,:]), y_stack)
        ax.fill_between(x, 0, y_stack[0, :], facecolor="red", alpha=.7, label=legend[0])
        ax.fill_between(x, y_stack[0, :], y_stack[1, :], facecolor="green", alpha=.7, label=legend[1])
        ax.fill_between(x, y_stack[1, :], y_stack[2, :], facecolor="blue", alpha=.7, label=legend[2])
        ax.fill_between(x, y_stack[2, :], y_stack[3, :], facecolor="magenta", alpha=.7, label=legend[3])
        ax.fill_between(x, y_stack[3, :], y_stack[4, :], facecolor="cyan", alpha=.7, label=legend[4])
        [ax.plot([-100]*len(x), color=colour, alpha=.9, label="estado%d" % index, linewidth=2)
         for index, colour in enumerate(color[1:])]
        ax.legend(ncol=3, loc="upper left")
        # ax.margins(0.1)  # derivative_data = [d*10+20 for d in derivative_data]
        ax2 = ax.twinx()
        ax2.set_xlim(0, min(500, x[-1]))
        # ax2.set_xlim(0, min(500, derivative_data[-1][-1][0]))
        ax2.set_ylim(-1, 1)        # ax.ylim(-5, 5)
        # ax.set_xlim(0, min(1028, derivative_data[-1][-1][0]))
        ax2.add_collection(lc)
        ax2.set_ylabel('colored states', color='r')

        # def make_proxy(zvalue, scalar_mappable, **kwargs):
        #     color = scalar_mappable.cmap(scalar_mappable.norm(zvalue))
        #     return Line2D([0, 1], [0, 1], color=color, **kwargs)
        # proxies = [make_proxy(item, lc, linewidth=5) for item in z]
        # ax.legend(proxies, ['Line 1', 'Line 2', 'Line 3', 'Line 4'])
        #
        # fig1.colorbar(lc)

        # plt.legend(["SEG"] + [plot for plot in CARDS], ncol=5, bbox_to_anchor=(0, 1, 1, 3),
        #            loc=3, borderaxespad=1.2, mode="expand")
        plt.subplots_adjust(bottom=0.08, left=.05, right=.96, top=.9, hspace=.35)
        fig1.savefig("statrans/%s.jpg" % "_".join(u_name.split()))
        # plt.show()


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
    # MinutiaConnections().load_from_db().generate_connecion_table_for_user()
    MinutiaProfiler().load_from_db().collect_state_burst_information()
    # MinutiaProfiler().load_from_db().survey_orc_transitivity_in_time()
    # # MinutiaProfiler().load_from_db().plot_derivative_marked_states()
    # # MinutiaProfiler().load_from_db().profile_wave_case_for_all_events()
    # # MinutiaStats().load_from_db().scan_for_minutia_stats_for_each_user()
    # # Track().load_from_db().scan_full_data_for_minutia_count_in_user_and_games(slicer=6, span=1256)
    # # Learn().load_from_db().replace_resampled_user_deltas_games_cards().write_db()
    # # Learn().load_from_db().build_interpolated_derivative_minutia_as_timeseries(slicer=12, threshold=8)
    # # Learn().load_from_db().resample_user_deltas()
