# -*- coding: UTF8 -*-
# import operator
import os
from csv import writer

import matplotlib.pyplot as plt
import pywt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib import colors as mcolors
import numpy as np
from tinydb import TinyDB, Query
from matplotlib import collections as mc
from math import log, exp

# import operator
# from datetime import datetime as dt
# from datetime import timedelta as td
# from time import strftime
# import matplotlib.pyplot as plt
from analisys.learn import Track, User
from analisys.minutia import MinutiaProfiler

NONE = ""
BTITLE = "Cognogram"

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
INDEX_GAME = {key + 1: value for key, value in enumerate("_Chaves_ _Mundo_ _FALA_ __A_T_I_V_A__".split())}
NAMED_GAME = "None _Chaves_ _Mundo_ _FALA_".split()
WAVELET_MODE = pywt.MODES.sp1
MACHINE_ORDER = [0, 2, 3, 1, 5, 4, 6, 7]
CLAZ_INDEX = {key: value + 4 for value, key in enumerate("VSFE")}


class Clazz:
    def __init__(self, claz, filtered):
        self.claz, self.filtered = claz, lambda stat: True if filtered is None else (stat.clazz == filtered)


CLZ_FILTER = {claz[1]: Clazz(claz, claz[1]) for claz in
              ' Verdadeiro Sucesso, Sucesso Mínimo, Falso Sucesso, Expulsão Simbólica'.split(',')}
NO_FILTER = Clazz(' Populacional', None)


class Lexicon:
    lex = {}
    common_vocabulary = "02 01 021 012 06 05 04 03 016".split()

    # common_vocabulary = "02 01 021 012 06 03 04 05 0212 0121".split()

    def __init__(self, headword, start_time, timestamp, user, clazz, game):

        class LexStats:
            def __init__(self, headword, count, latency, interval, permanence):
                self.headword, self.count, self.latency, self.interval, self.permanence = \
                    headword, count, latency, interval, permanence
                self.timestamp = []

            def update(self, timestamp, start_time):
                self.count += 1
                self.latency = min(self.latency, start_time)
                self.interval.append(timestamp - self.timestamp[-1] if self.timestamp else timestamp)
                self.timestamp.append(timestamp)
                self.permanence.append(timestamp - start_time)

        self.headword, self.start_time, self.timestamp, self.user, self.clazz, self.game = \
            headword, start_time, timestamp, user, clazz, game
        if user not in Lexicon.lex:
            stats = {headword: LexStats(headword=headword, count=0, latency=4e3, interval=[], permanence=[])
                     for headword in Lexicon.common_vocabulary}
            Lexicon.lex[user] = dict(lex=[self], stats=stats)
        else:
            Lexicon.lex[user]["lex"].append(self)
            if headword in Lexicon.common_vocabulary:
                Lexicon.lex[user]["stats"][headword].update(timestamp, start_time)

    @staticmethod
    def survey():
        from statistics import mean

        # for lex_user in Lexicon.lex_users:
        #     for lex in Lexicon.lex[lex_user]:
        #         if lex.headword in Lexicon.common_vocabulary:
        #             lex["stats"][lex.headword].update(lex.timestamp, lex.start_time)
        stats_by_lex = [
            list(zip(*[(lexentry["stats"][headword].count, lexentry["stats"][headword].latency,
                        mean(lexentry["stats"][headword].interval) if lexentry["stats"][headword].interval else 0,
                        mean(lexentry["stats"][headword].permanence) if lexentry["stats"][
                            headword].permanence else 0)
                       for lexentry in Lexicon.lex.values()]))
            for headword in Lexicon.common_vocabulary]
        print("Lexicon.lex.", [(l, Lexicon.lex[l]) for l in Lexicon.lex])
        print("stats_by_lex", stats_by_lex)
        stat_props = [(count, latency, interval, permanence)
                      for count, latency, interval, permanence in stats_by_lex]
        return list(zip(*stat_props)), \
               ["%s do Vocabulário" % stat for stat in "Contagem Latência Intervalo Permanência".split()], \
               Lexicon.common_vocabulary, " coletivo"


class Idiomaton:
    idiom = {}
    idiomaton = {}
    common_idiomatics = ('0261', '051', '041', '025', '062', '0212')

    # common_idiomatics = ('072', '0242', '013', '0162', '0261', '0412', '0512', '014', '0252', '051', '015',
    #                      '02121', '024', '041', '025', '061', '026', '062', '0121', '0212')
    # common_idiomatics = ('0412', '0302', '051', '0501', '0601', '0106', '020121', '0205', '0204', '01021', '02101',
    #                      '020212', '01012', '0206', '01202', '02102', '02021', '0102', '0201')
    # # common_idiomatics = ('051', '0601', '0501', '020121', '01201', '01021', '0204', '02101', '020212',
    # #                      '0206', '01012', '02102', '02012', '02021', '0102', '0201')

    def __init__(self, headword, start_time, timestamp, user, clazz, game):

        class IdiomStats:
            def __init__(self, headword, count, latency, interval, permanence):
                self.headword, self.count, self.latency, self.interval, self.permanence = \
                    headword, count, latency, interval, permanence
                self.timestamp = []

            def update(self, timestamp, start_time):
                self.count += 1
                self.latency = min(self.latency, start_time)
                self.interval.append(timestamp - self.timestamp[-1] if self.timestamp else timestamp)
                self.timestamp.append(timestamp)
                self.permanence.append(timestamp - start_time)

        self.headword, self.start_time, self.timestamp, self.user, self.clazz, self.game = \
            headword, start_time, timestamp, user, clazz, game
        if user not in Idiomaton.idiom:
            stats = {
                headword: IdiomStats(headword=headword, count=0, latency=2.5e3, interval=[], permanence=[])
                for headword in Idiomaton.common_idiomatics}
            Idiomaton.idiom[user] = dict(idiom=[self], stats=stats)
        else:
            Idiomaton.idiom[user]["idiom"].append(self)
            if headword in Idiomaton.common_idiomatics:
                Idiomaton.idiom[user]["stats"][headword].update(timestamp, start_time)

    def update_idiom(self, idiom, popul, _Chaves_=0, _Mundo_=0, _FALA_=0, V=0, S=0, F=0, E=0):
        # idiom, popul, _Chaves_=0, _Mundo_=0, _FALA_=0, V=0, S=0, F=0, E=0
        Idiomaton.idiom[idiom]

    @staticmethod
    def survey(filtered=NO_FILTER):
        from statistics import mean

        # for lex_user in Lexicon.lex_users:
        #     for lex in Lexicon.lex[lex_user]:
        #         if lex.headword in Lexicon.common_vocabulary:
        #             lex["stats"][lex.headword].update(lex.timestamp, lex.start_time)
        stats_by_lex = [
            list(zip(*[(idiom_entry["stats"][headword].count, idiom_entry["stats"][headword].latency,
                        mean(idiom_entry["stats"][headword].interval) if idiom_entry["stats"][headword].interval else 0,
                        mean(idiom_entry["stats"][headword].permanence) if idiom_entry["stats"][
                            headword].permanence else 0)
                       for idiom_entry in Idiomaton.idiom.values() if filtered.filtered(idiom_entry["idiom"][0])]))
            # for idiom_entry in Idiomaton.idiom.values() if idiom_entry["idiom"][0].clazz == "E"]))
            for headword in Idiomaton.common_idiomatics]
        print("Lexicon.lex.", [(l, Idiomaton.idiom[l]) for l in Idiomaton.idiom])
        print("stats_by_lex", stats_by_lex)
        stat_props = [
            (count, latency, interval,
             permanence)
            for count, latency, interval, permanence in stats_by_lex]
        return list(zip(*stat_props)), \
               ["%s do Idiomático" % stat for stat in "Contagem Latência Intervalo Permanência".split()], \
               Idiomaton.common_idiomatics, filtered.claz, "Índices dos idiomas EICA"


class Logicon:
    logic = {}
    logicon = {}
    common_logics = ['0212', '041', '051', '0261', '062', '025']

    # common_logics = ('0502', '020101012', '01201', '020101021', '01020201', '0602', '02012')
    # common_idiomatics = ('051', '0601', '0501', '020121', '01201', '01021', '0204', '02101', '020212',
    #                      '0206', '01012', '02102', '02012', '02021', '0102', '0201')

    def __init__(self, headword, sequence, start_time, timestamp, user, clazz, game):

        class LogicStats:
            def __init__(self, headword, count, latency, interval, permanence):
                self.headword, self.count, self.latency, self.interval, self.permanence = \
                    headword, count, latency, interval, permanence
                self.timestamp = []

            def update(self, timestamp, start_time):
                self.count += 1
                self.latency = min(self.latency, start_time)
                self.interval.append(timestamp - self.timestamp[-1] if self.timestamp else timestamp)
                self.timestamp.append(timestamp)
                self.permanence.append(timestamp - start_time)

        self.headword, self.sequence, self.start_time, self.timestamp, self.user, self.clazz, self.game = \
            headword, sequence, start_time, timestamp, user, clazz, game
        if user not in Logicon.logic:
            stats = {
                headword: LogicStats(headword=headword, count=0, latency=2.5e3, interval=[], permanence=[])
                for headword in Logicon.common_logics}
            Logicon.logic[user] = dict(logic=[self], stats=stats)
        else:
            Logicon.logic[user]["logic"].append(self)
            if headword in Logicon.common_logics:
                Logicon.logic[user]["stats"][headword].update(timestamp, start_time)

    @staticmethod
    def survey(filtered=NO_FILTER):
        from statistics import mean

        # for lex_user in Lexicon.lex_users:
        #     for lex in Lexicon.lex[lex_user]:
        #         if lex.headword in Lexicon.common_vocabulary:
        #             lex["stats"][lex.headword].update(lex.timestamp, lex.start_time)
        stats_by_lex = [
            list(zip(*[(logic_entry["stats"][headword].count, logic_entry["stats"][headword].latency,
                        mean(logic_entry["stats"][headword].interval) if logic_entry["stats"][headword].interval else 0,
                        mean(logic_entry["stats"][headword].permanence) if logic_entry["stats"][
                            headword].permanence else 0)
                       for logic_entry in Logicon.logic.values() if filtered.filtered(logic_entry["logic"][0])]))
            # for idiom_entry in Idiomaton.idiom.values() if idiom_entry["logic"][0].clazz == "E"]))
            for headword in Logicon.common_logics]
        print("Logicon.logic.", [(l, Logicon.logic[l]) for l in Logicon.logic])
        print("stats_by_lex", stats_by_lex)
        stat_props = [
            (count, latency, interval,
             permanence)
            for count, latency, interval, permanence in stats_by_lex] if any(stats_by_lex) else \
            [(0, 2.5e3, 0, 0), (1, 1.5e3, 1, 1)]
        ticks = [Logicon.logicon[burst]["sequence"] for burst in Logicon.common_logics]
        return list(zip(*stat_props)), \
               ["%s da Lógica" % stat for stat in "Contagem Latência Intervalo Permanência".split()], \
               ticks, filtered.claz, "Índices das lógicas EICA"


class LanguageSurvey(MinutiaProfiler):
    def scan_for_minutia_stats_in_users(self, slicer=16):
        """
        Rastreia a série temporal de cada usuário e levanta estatísticas sobre as minúcias derivativas.

        :param slicer: recorta os dados neste tamanho
        :return:
        """
        import numpy as np

        def sigla(name, _=""):
            return ' '.join(n.capitalize() if i == 0 else n.capitalize()[0] + "."
                            for i, n in enumerate(name.split()))[:10]

        def wavelenght(mt):
            if not mt:
                return [np.nan, np.nan]
            minutia_events = mt[:]
            minutia_intervals = [j - i for i, j in zip(minutia_events, minutia_events[1:]) if j - i >= 4]
            minutia_events = [minutia_events[0] - 4] + minutia_events + [minutia_events[-1] + 4]
            end_start_pairs = [(i, j) for i, j in zip(minutia_events, minutia_events[1:]) if j - i >= 5]
            minutia_durations = [b - a + 4 for (_, a), (b, _) in zip(end_start_pairs, end_start_pairs[1:])]
            print(minutia_intervals, minutia_durations)
            duration_average = sum(minutia_durations) / len(minutia_durations) if minutia_durations else np.nan
            interval_average = sum(minutia_intervals) / len(minutia_intervals) if minutia_intervals else np.nan
            return [interval_average, duration_average]

        alldata = []
        printdata = []
        self.isoclazz_minutia_buckets = {}
        User.iso_classifier = {}
        isoclazz = []
        for user in self.user:
            if len(user.jogada) < 4:
                continue
            user.minutia_buckets = {minutia_id: [] for minutia_id in range(40)}
            user.resample_user_deltas_games()
            user.scan_resampled_minutia(isoclazz, slicer, self.isoclazz_minutia_buckets, user.track_minutia_event)
        for user in self.user:
            if len(user.jogada) < 4:
                continue
            # print(user.user, user.minutia_buckets)
            ub = user.minutia_buckets
            # wavelenght=[sum(b-a for a, b in zip(mt, mt[1:]))/len(mt) if mt else 0 for mt in ub.values()]
            _ = "{:<40}: dmt:{:<3} cm0:{:<3} tm0:{:<3} dm0:{:<3}"
            mfm = "{:<10}: dmt:{:<3} " + "".join(["cm%d:{:<3} dm%d:{:<3} wv%d:{:<3} " % ((i,) * 3) for i in range(8)])
            data = [[len(mt), min(mt) if len(mt) else np.nan, *wavelenght(mt)] for mt in ub.values()]
            ndata = []
            for d in data[:8]:
                ndata.extend(d)
            # if all(len(mt)>1 for i, mt in ub.items() if i <6):
            alldata.append(ndata)
            ndata = [sigla(user.user), max(min(m) if m else 0 for m in ub.values())] + ndata
            printdata.append(ndata)
            print(mfm.format(*ndata))
        # self.plot_derivative_minutia_by_prognostics_games()
        """
        columns = zip(*alldata)
        stats = [sum(st) // len(st) for i, st in enumerate(columns) if i > 0]
        columns = zip(*alldata)
        conta = [(sum(count) // len(count), i) for i, (count, delay, wave) in
                 enumerate(list(zip(*(iter(columns),) * 3)))]
        conta.sort(reverse=True)
        print("contagem de minúcias", conta)
        columns = zip(*alldata)
        atraso = [(sum(delay) // len(delay), i) for i, (count, delay, wave) in
                  enumerate(list(zip(*(iter(columns),) * 3)))]
        atraso.sort()
        print("atraso para aparecer a minúcia", atraso)
        columns = zip(*alldata)
        onda = [(sum(wave) // len(wave), i) for i, (count, delay, wave) in enumerate(list(zip(*(iter(columns),) * 3)))]
        onda.sort()
        print("distância (comprimento de onda) em tempo entre mesma minúcia", onda)
        printdata.append(["total"] + stats)
        # reordena_minucias_por_atraso = [delay[1] for delay in atraso]
        """
        reordena_minucias_por_atraso = [0, 2, 3, 1, 5, 4, 6, 7]
        columns = zip(*alldata)
        estatisticas_ordenadas = list(zip(*(iter(columns),) * 4))
        print("reordena_minucias_por_atraso", reordena_minucias_por_atraso, len(estatisticas_ordenadas))
        # return
        estatisticas_ordenadas = [estatisticas_ordenadas[sort_order] for sort_order in reordena_minucias_por_atraso]
        contagems = [contagem for contagem, atraso, _, _ in estatisticas_ordenadas]
        print("reordena_minucias_por_atraso contagems", contagems[-1])
        atrasos = [[w for w in atraso if w is not np.nan] for _, atraso, _, _ in estatisticas_ordenadas]
        print("reordena_minucias_por_atraso atrasos", atrasos[-1])
        intervals = [[w for w in wavelenght if w is not np.nan] for _, atraso, wavelenght, _ in estatisticas_ordenadas]
        duration = [[w for w in wavelenght if w is not np.nan] for _, atraso, _, wavelenght in estatisticas_ordenadas]
        print("reordena_minucias_por_atraso wavelenghts", intervals[-1], np.nan not in intervals[-1])
        estatisticas_ordenadas = [contagems, atrasos, intervals, duration]

        estatisticas = estatisticas_ordenadas
        # print(mfm.format(*[x for line in estatisticas_ordenadas for x in line]))
        labels = 'Contagem de estados,Latência de estados,Intervalo entre estados,Permanência no estado'.split(",")
        self.boxplot_de_caracteristicas(estatisticas, labels, ticks=["eica%d" % order for order in range(8)])
        # self.boxplot_de_caracteristicas(atraso)
        import analisys.invariant as inv
        # head = "aluno,atr,"+"".join(["cm%d,tm%d,dm%d,wv%d," % ((i,)*4) for i in range(4)])
        head = "aluno,atr," + "".join(["cm%d,dm%d,wv%d," % ((i,) * 3) for i in range(8)])
        printdata.append(head.split(","))
        inv.htmltable(data=printdata, head=head.split(","), foot="",
                      caption="Contagem, atraso e intervalo de minúcias", filename="stats_minutia.html")
        print("countuser_minutia_buckets", sum(count for user in self.user for count in user.minutia_buckets))
        print("sumuser_minutia_buckets", sum(1 for user in self.user if any(user.minutia_buckets)))
        # self.plot_derivative_minutia_by_user()
        return
        # plt.imshow(zi, vmin=min(z), vmax=max(z), origin='lower',
        #            extent=[min(x), max(x), min(y), max(y)])
        # plt.scatter(x, y, c=z)
        # plt.colorbar()
        # plt.show()

    def mark_state_use_cases_for_users(self, named_user=None, plot=True):
        state_use_case = {}
        user_index = []
        for turn in self.scan_states_in_full_data():
            # print(user_data[0][-1])
            for state, _, _0, clz, _2, user in turn:

                if (clz, user) not in user_index:
                    user_index.append((clz, user))
                user = user_index.index((clz, user))
                state_use_case[user] = state_use_case.get(user, {})
                state_use_case[user][state] = state_use_case[user].get(state, 0) + 1
                state_use_case[user][0] = CLAZ_INDEX.get(clz, 1)*10.0  # show cognition class at state zero
        reindex = [(CLAZ_INDEX.get(clz, 0), ind) for ind, (clz, _) in enumerate(user_index)]
        reindex.sort()  # sort participants by cognition class
        state_use_case = [list(zip(*[[state, log(state_use_case[user][state])] for state in state_use_case[user]]))
                          for clz, user in reindex]

        print(state_use_case)
        if plot:
            self.cognomogram_histogram_user_vs_state(state_use_case)
        return state_use_case

    def mark_vocabulary_use_cases(self, named_user=None, plot=False):
        # user_data = [user for user in self.scan_states_in_full_data()]
        for user_data, user_object in self.scan_states_in_full_data_plus_user():
            # print(user_data[0][-1])
            if named_user and named_user != user_data[0][-1]:
                continue
            # states, time, data, _, _, user = zip(*user_data)
            user_collected_burst = "0"
            start_time = 0
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
                        Lexicon(user_collected_burst, start_time, time, user_data[0][-1], claz, jogo)
                        user_collected_burst = "0"
                        start_time = time
                else:
                    user_collected_burst += "" if str(state - 1) == user_collected_burst[-1] else str(state - 1)
        best_burst = [(g, k, c, m, r, v, f, s, e) for k, (g, c, m, r, v, f, s, e) in self.state_burst.items() if g > 1]
        best_burst = [(g, k, c, m, r, v, f, s, e) for k, (g, c, m, r, v, f, s, e) in self.state_burst.items()
                      if sum(1 for count in [v, f, s, e] if count) > 2]
        best_burst.sort()
        gcount, labels, c, m, r, v, f, s, e = zip(*best_burst)
        print("plot_burst_usage_and_size, lex", labels)
        if plot:
            self.plot_burst_usage_and_size([labels, gcount, c, m, r, v, s, f, e])
            # print("collect_state_burst_information", len(self.state_burst), len(best_burst), best_burst)

    def mark_idiom_use_cases(self, named_user=None, plot=False):
        # user_data = [user for user in self.scan_states_in_full_data()]
        for user_name, current_user in Lexicon.lex.items():
            # print(user_data[0][-1])
            if named_user and named_user != user_name:
                continue
            # states, time, data, _, _, user = zip(*user_data)
            user_collected_burst = ""
            started_time = 0
            # print(list(current_user.__dict__[arg] for arg in
            #          "headword, start_time, timestamp, user, clazz, game".split(", ")))
            for user_stat in current_user["lex"]:
                headword, start_time, timestamp, user, clazz, game = \
                    list(user_stat.__dict__[arg] for arg in
                         "headword, start_time, timestamp, user, clazz, game".split(", "))
                print("headword, start_time, timestamp, user, clazz, game", headword, start_time, timestamp, user,
                      clazz, game)
                # user_collected_burst = headword + next_stat.headword

                if headword in Lexicon.common_vocabulary:
                    if user_collected_burst != "" and (user_collected_burst not in Lexicon.common_vocabulary):
                        if user_collected_burst in Idiomaton.idiomaton:
                            ucb = Idiomaton.idiomaton[user_collected_burst]
                        else:
                            ucb = Idiomaton.idiomaton[user_collected_burst] = dict(
                                popul=0, _Chaves_=0, _Mundo_=0, _FALA_=0, V=0, S=0, F=0, E=0)
                        Idiomaton.idiomaton[user_collected_burst]["popul"] += 1
                        Idiomaton.idiomaton[user_collected_burst][NAMED_GAME[int(game)]] += 1
                        if clazz:
                            Idiomaton.idiomaton[user_collected_burst][clazz] += 1
                        Idiomaton(user_collected_burst, started_time, timestamp, user_name, clazz, game)
                        user_collected_burst = ""
                        started_time = timestamp
                else:
                    user_collected_burst += "" if user_collected_burst.endswith(headword) else headword
        # print("Idiomaton.idiomaton", Idiomaton.idiomaton)
        kind = ['popul', '_Chaves_', '_Mundo_', '_FALA_', 'V', 'S', 'F', 'E']
        # best_burst = [list(stats[stat] for stat in kind)+[k] for k, stats in Idiomaton.idiomaton.items() if
        #               stats['popul'] > 3]
        best_burst = [list(stats[stat] for stat in kind) + [k] for k, stats in Idiomaton.idiomaton.items() if
                      (sum(1 for claz in ['V', 'S', 'F', 'E'] if stats[claz]) > 2) and
                      (sum(1 for jogo in ['_Chaves_', '_Mundo_', '_FALA_'] if stats[jogo]) > 2)]
        best_burst.sort()
        gcount, c, m, r, v, s, f, e, labels = zip(*best_burst)
        if plot:
            self.plot_burst_usage_and_size(
                [labels, gcount, c, m, r, v, s, f, e],
                title="Contagem da transitividade idiomática", log=0)
            print("plot_burst_usage_and_size labels", labels)
            # print("collect_state_burst_information", len(self.state_burst), len(best_burst), best_burst)

    def mark_logic_use_cases(self, named_user=None, plot=False):
        # user_data = [user for user in self.scan_states_in_full_data()]
        for user_name, current_user in Idiomaton.idiom.items():
            # print(user_data[0][-1])
            if named_user and named_user != user_name:
                continue
            # states, time, data, _, _, user = zip(*user_data)
            user_collected_burst = ""
            started_time = 0
            # print(list(current_user.__dict__[arg] for arg in
            #          "headword, start_time, timestamp, user, clazz, game".split(", ")))
            for user_stat in current_user["idiom"]:
                headword, start_time, timestamp, user, clazz, game = \
                    list(user_stat.__dict__[arg] for arg in
                         "headword, start_time, timestamp, user, clazz, game".split(", "))
                print("headword, start_time, timestamp, user, clazz, game", headword, start_time, timestamp, user,
                      clazz, game)
                # user_collected_burst = headword + next_stat.headword

                if headword in Idiomaton.common_idiomatics:
                    if user_collected_burst != "" and (user_collected_burst not in Idiomaton.common_idiomatics) \
                            and (user_collected_burst not in Lexicon.common_vocabulary):
                        sequence, user_collected_burst = user_collected_burst, headword
                        if user_collected_burst in Logicon.logicon:
                            ucb = Logicon.logicon[user_collected_burst]
                        else:
                            ucb = Logicon.logicon[user_collected_burst] = dict(
                                popul=0, _Chaves_=0, _Mundo_=0, _FALA_=0, V=0, S=0, F=0, E=0)
                        Logicon.logicon[user_collected_burst]["sequence"] = sequence
                        Logicon.logicon[user_collected_burst]["popul"] += 1
                        Logicon.logicon[user_collected_burst][NAMED_GAME[int(game)]] += 1
                        if clazz:
                            Logicon.logicon[user_collected_burst][clazz] += 1
                        Logicon(user_collected_burst, sequence, start_time, timestamp, user_name, clazz, game)
                        user_collected_burst = ""
                        start_time = timestamp
                else:
                    user_collected_burst += "" if user_collected_burst.endswith(headword) else headword
        # print("Logicon.logicon", Logicon.logicon)
        kind = ['popul', '_Chaves_', '_Mundo_', '_FALA_', 'V', 'S', 'F', 'E']
        # best_burst = [list(stats[stat] for stat in kind)+[k] for k, stats in Logicon.logicon.items() if
        #               stats['popul'] > 3]
        best_burst = [list(stats[stat] for stat in kind) + [stats["sequence"]] for k, stats in Logicon.logicon.items()
                      if
                      sum(1 for claz in ['V', 'S', 'F', 'E'] if stats[claz]) > 0]
        best_burst.sort()
        gcount, c, m, r, v, s, f, e, labels = zip(*best_burst)
        if plot:
            self.plot_burst_usage_and_size([labels, gcount, c, m, r, v, s, f, e], log=0)
            print("plot_burst_usage_and_size labels", [k for k in Logicon.logicon.keys()])
            # print("collect_state_burst_information", len(self.state_burst), len(best_burst), best_burst)

    def survey_vocabulary_use_in_population(self, plot=True):
        self.mark_vocabulary_use_cases(plot=plot)
        if not plot:
            self.boxplot_de_caracteristicas(*Lexicon.survey())

    def survey_idiom_use_in_population(self, plot=True, filtered=NO_FILTER):
        self.mark_vocabulary_use_cases()
        self.mark_idiom_use_cases(plot=plot)
        if not plot:
            self.boxplot_de_caracteristicas(*Idiomaton.survey(filtered))

    def survey_logic_use_in_population(self, plot=True, filtered=NO_FILTER):
        self.mark_vocabulary_use_cases()
        self.mark_idiom_use_cases(plot=False)
        self.mark_logic_use_cases(plot=plot)
        if not plot:
            self.boxplot_de_caracteristicas(*Logicon.survey(filtered))

    def scan_for_minutia_stats_for_each_user(self, slicer=16):
        """
        Rastreia a série temporal de cada usuário e levanta estatísticas sobre as minúcias derivativas.

        :param slicer: recorta eos dados neste tamanho
        :return:
        """
        import numpy as np

        def sigla(name, _=""):
            return '_'.join(n.capitalize() if i == 0 else n.capitalize()[0] + "_"
                            for i, n in enumerate(name.split()))[:10]

        def wavelenght(mt):
            empty = [0, 1]
            if not mt:
                return empty * 2
            minutia_events = mt[:]
            minutia_intervals = [j - i for i, j in zip(minutia_events, minutia_events[1:]) if j - i >= 4]
            minutia_events = [minutia_events[0] - 4] + minutia_events + [minutia_events[-1] + 4]
            end_start_pairs = [(i, j) for i, j in zip(minutia_events, minutia_events[1:]) if j - i >= 5]
            minutia_durations = [b - a + 4 for (_, a), (b, _) in zip(end_start_pairs, end_start_pairs[1:])]
            print("minutia_intervals", minutia_intervals, minutia_durations)
            minutia_intervals += empty * (2 - len(minutia_intervals))
            minutia_durations += empty * (2 - len(minutia_durations))
            minutia_latency = [0, min(minutia_events)]
            minutia_count = [0, len(minutia_events)]
            return [minutia_count, minutia_latency, minutia_intervals, minutia_durations]

        printdata = []
        self.isoclazz_minutia_buckets = {}
        User.iso_classifier = {}
        isoclazz = []
        reordena_minucias_por_atraso = [0, 2, 3, 1, 5, 4, 6, 7]
        for user in self.user:
            if len(user.jogada) < 4:
                continue
            user.minutia_buckets = {minutia_id: [] for minutia_id in range(40)}
            user.resample_user_deltas_games()
            user.scan_resampled_minutia(isoclazz, slicer, self.isoclazz_minutia_buckets, user.track_minutia_event)
        for user in self.user:
            alldata = []
            if len(user.jogada) < 4:
                continue
            # print(user.user, user.minutia_buckets)
            ub = user.minutia_buckets
            data = [wavelenght(mt) for mt in ub.values()]
            ndata = []
            for d in data[:8]:
                ndata.extend(d)
            # if all(len(mt)>1 for i, mt in ub.items() if i <6):
            data = [data[sort_order] for sort_order in reordena_minucias_por_atraso if sort_order < len(data)]
            columns = zip(*data)
            estatisticas_ordenadas = list(zip(*(iter(columns),) * 2))
            print("reordena_minucias_por_atraso", reordena_minucias_por_atraso, len(estatisticas_ordenadas))
            # return
            estatisticas_ordenadas = [estatisticas_ordenadas[sort_order] for sort_order in reordena_minucias_por_atraso
                                      if sort_order in estatisticas_ordenadas]
            intervals = [[w for w in wavelenght if w is not np.nan] for wavelenght, _ in estatisticas_ordenadas]
            print("reordena_minucias_por_atraso atrasos", intervals)
            duration = [[w for w in wavelenght if w is not np.nan] for _, wavelenght in estatisticas_ordenadas]
            print("reordena_minucias_por_atraso wavelenghts", duration)
            estatisticas_ordenadas = [intervals if len(intervals) > 1 else [0, 1],
                                      duration or [0] if len(duration) > 1 else [0, 1]]

            estatisticas = list(zip(*data))
            print(data)
            labels = 'Intervalo entre estados,Permanência no estado'.split(",")
            labels = 'Contagem de estados,Latência de estados,Intervalo entre estados,Permanência no estado'.split(",")
            # print(mfm.format(*[x for line in estatisticas_ordenadas for x in line]))
            ticks = ["eica%d" % order for order, _ in enumerate(estatisticas)]
            self.boxplot_de_caracteristicas(estatisticas, labels, ticks, filename="violin/" + sigla(user.user))

    @staticmethod
    def _boxplot_de_caracteristicas(data, filename=None):
        plt.figure(1)
        for prop, caracteristic in enumerate(data):
            plt.subplot(311 + prop)

            box = plt.boxplot(caracteristic, notch=True, patch_artist=True)

            colors = ['tan', 'pink', 'orange', 'yellow', 'lightgreen', 'lightblue', 'cyan', 'purple']
            for patch, color in zip(box['boxes'], colors):
                patch.set_facecolor(color)
        if filename:
            plt.savefig(filename + ".png")
        else:
            plt.show()

    @staticmethod
    def _violinplot_de_caracteristicas(data, filename=None):
        plt.figure(1)
        for prop, caracteristic in enumerate(data):
            plt.subplot(311 + prop)

            box = plt.boxplot(caracteristic, notch=True, patch_artist=True)

            # colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink']
            colors = ['tan', 'pink', 'orange', 'yellow', 'lightgreen', 'lightblue', 'cyan', 'purple']
            for patch, color in zip(box['boxes'], colors):
                patch.set_facecolor(color)

        plt.show()

    @staticmethod
    def boxplot_de_caracteristicas(data, labels, ticks, complemento=" individual",
                                   xlabel='Índices dos estados eica', filename=None):
        # labels = 'Contagem de estados,Latência de estados,Intervalo entre estados,Permanência no estado'.split(",")

        # colors = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink']
        colors = ['tan', 'pink', 'orange', 'yellow', 'lightgreen',
                  'aquamarine', 'cyan', 'lightblue', 'violet', 'fuchsia'] if len(ticks) <= 10 else [
            'tan', 'lightcoral', 'pink', 'orange', 'yellow', 'yellowgreen', 'olive', 'lightgreen',
            'springgreen', 'aquamarine', 'cyan', 'lightblue', 'skyblue', 'violet', 'orchid', 'fuchsia'
        ] if len(ticks) <= 16 else [
            'tan', 'salmon', 'lightcoral', 'pink', 'orange', 'yellow', 'lawngreen', 'yellowgreen', 'olive',
            'lightgreen', 'springgreen', 'mediumaquamarine', 'aquamarine', 'cyan', 'paleturquoise', 'lightblue',
            'skyblue', 'violet', 'orchid', 'fuchsia', 'grey'
        ]
        edges = ['maroon', 'red', 'orangered', 'goldenrod', 'green',
                 'teal', 'deepskyblue', 'blue', 'darkviolet', 'darkmagenta'] if len(ticks) <= 10 else [
            'maroon', 'tomato', 'red', 'orangered', 'goldenrod', 'greenyellow', 'darkolivegreen', 'green',
            'forestgreen', 'teal', 'deepskyblue', 'blue', 'navy', 'darkviolet', 'darkmagenta', 'indigo'
        ] if len(ticks) <= 16 else [
            'maroon', 'brown', 'tomato', 'red', 'orangered', 'goldenrod', 'greenyellow', 'darksage',
            'darkolivegreen', 'green', 'forestgreen', 'teal', 'deepskyblue', 'cornflowerblue', 'blue',
            'navy', 'darkviolet', 'darkmagenta', 'indigo', 'k'
        ]

        fig, axes = plt.subplots(nrows=len(labels), ncols=1, figsize=(8, 12))
        # fig.tight_layout()
        for prop, (caracteristic, ax, label) in enumerate(zip(data, axes, labels)):
            # plt.subplot(311+prop)

            box = ax.violinplot(caracteristic, showmeans=False, showmedians=True)
            ax.yaxis.grid(True)
            ax.set_xticks([y + 1 for y in range(len(data))])
            ax.set_xlabel(xlabel)
            ax.set_title(label + complemento)
            ax.set_ylabel(label)
            print(colors, edges, ticks, len(ticks))
            for patch, edge, color in zip(box['bodies'], edges, colors):
                patch.set_facecolor(color)
                patch.set_edgecolor(edge)
                patch.set_linewidth(3)
        plt.subplots_adjust(hspace=0.5)
        plt.setp(axes, xticks=[y + 1 for y in range(len(ticks))],
                 xticklabels=['%s' % tick for tick in ticks])
        if filename:
            plt.savefig(filename + ".png")
        else:
            plt.show()

    @staticmethod
    def cognomogram_histogram_user_vs_state(ubars, title=BTITLE, log=1):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ucolor = [(r, g, b) for r in range(50, 250, 50) for g in range(50, 250, 50) for b in range(0, 250, 50)]
        colors = [["#"+''.join('%02x' % i for i in rgb), usr] for usr, rgb in enumerate(ucolor)]
        print(colors[:9])
        color_index = {usr: "#"+''.join('%02x' % i for i in rgb) for usr, rgb in enumerate(ucolor)}
        # for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
        colors = [[color_index[usr], data] for usr, data in enumerate(ubars[:90])]

        for z, (c, d) in enumerate(colors):
            xs = np.arange(8)
            ys = np.random.rand(8)
            xs, ys = d

            # You can provide either a single color or an array. To demonstrate this,
            # the first bar of each set will be colored cyan.
            cs = [c] * len(xs)
            cs[0] = "rgbcmrgbcm"[int((exp(ys[0]))//10)]
            # cs[0] = 'c'
            ax.bar(xs, ys, zs=z, zdir='x', color=cs, alpha=0.5)
        ax.set_xlabel('Participants')
        # ax.set_xlim3d(0, 7)
        ax.set_ylabel('EICA States')
        ax.set_ylim3d(0, 9)
        ax.set_zlabel('States Count')
        ax.set_zlim3d(0, 7)
        # ax.set_zscale("log", nonposy='clip')

        plt.title(title)

        plt.show()
        return

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
    # LanguageSurvey().load_from_db().survey_logic_use_in_population(plot=False, filtered=NO_FILTER)
    # [LanguageSurvey().load_from_db().survey_logic_use_in_population(plot=False, filtered=CLZ_FILTER[c]) for c in "VSFE"]
    # LanguageSurvey().load_from_db().survey_idiom_use_in_population(plot=True, filtered=NO_FILTER)
    # [LanguageSurvey().load_from_db().survey_idiom_use_in_population(plot=False, filtered=CLZ_FILTER[c]) for c in "VSFE"]
    # LanguageSurvey().load_from_db().survey_vocabulary_use_in_population()
    LanguageSurvey().load_from_db().mark_state_use_cases_for_users()
    # # LanguageSurvey().load_from_db().scan_for_minutia_stats_in_users()
    # # LanguageSurvey().load_from_db().scan_for_minutia_stats_for_each_user()
