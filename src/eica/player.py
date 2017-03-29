#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa EICA
# Copyright 2014-2017 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://j.mp/GNU_GPL3>`__.
#
# EICA é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

"""Resources to be used in game.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from browser import timer, svg, doc
from braser.vitollino import Vitollino
from datetime import datetime as dt
from datetime import timedelta as td

NOT_CARTA = "__A_T_I_V_A__ minitens f_r_u_t_a o_b_j_e_t_o".split()
SX = 0.015
SY = 2


def parse_time(time):
    try:
        return dt.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return dt.strptime(time, "%Y-%m-%d %H:%M:%S")
    except TypeError:
        return time


class Ativadora:
    def __init__(self, evento, carta, ponto, player=lambda: None):
        self.evento, self.carta, self.ponto, self.player, = evento, carta, ponto, player
        self.casa = "0_0"

    def play(self, time, carta=None, casa=None):
        self.carta = carta if carta else self.carta
        self.casa = casa if casa else self.casa
        timer.set_timeout(self._play, time)

    def _play(self):
        carta = [int(carta) for carta in self.carta.split('_')] if self.carta not in NOT_CARTA else [0]
        casa = [int(casa) for casa in self.casa.split('_')]
        print("_play", casa, carta, self.casa, self.carta)
        self.evento(carta, casa)
        self.player()


class Fachada:
    def __init__(self):
        Vitollino.registry = self.registrar
        self.ativadores = {"_ABAS_": Ativadora(evento=lambda *_: None, carta=[0], ponto=[0, 0], player=self.play)}
        self.tape = []
        self.tempo = self.tempo0 = None
        self.deriva = 0
        self.count = 0
        self.delta = 500
        self.chart = doc["plotsvg"]
        self.point = (62.0, 200.0)
        # _ = self.chart <= svg.polyline(fill="none", stroke="#0074d9", strokeWidth="3",
        #                                points="60,220 120,160 140,180 160,120")

    def plot(self, points=None, fill="none", stroke="#0074d9", stroke_width="1"):
        if points is None:
            points = [0, 0]
        points = points[0] * SX + self.point[0], points[1] * SY + 200.0
        plotpoints = self.point + tuple(points)
        _ = self.chart <= svg.polyline(fill=fill, stroke=stroke, stroke_width=stroke_width,
                                       points="%f,%f %f,%f" % plotpoints)
        self.point = points

    def registrar(self, _, evento, carta, ponto):
        self.ativadores[ponto] = Ativadora(evento=evento, carta=carta, ponto=ponto, player=self.play)

    def player(self, tape=JSON, time=30, delta=500):
        self.tape = tape
        self.tempo = self.tempo0 = parse_time(self.tape[0]["tempo"]) - td(seconds=time)
        self.delta = delta
        self.play()

    def play(self):
        def record(ponto, carta, casa, tempo, **_):
            self.tempo, deltatempo = parse_time(tempo), parse_time(tempo) - self.tempo
            print("Fachada play deltatempo", deltatempo.total_seconds() * self.delta)
            tempo_corrente = self.tempo - self.tempo0
            self.deriva = deltatempo.total_seconds() - self.deriva
            if deltatempo.total_seconds() > 0.5:
                self.plot([tempo_corrente.total_seconds()+0.5, 0])
            # self.plot([tempo_corrente.total_seconds(), deltatempo.total_seconds()])
            self.plot([tempo_corrente.total_seconds(), self.deriva])
            self.ativadores[ponto].play(deltatempo.total_seconds() * self.delta, carta, casa)

        if self.count >= len(self.tape):
            return
        registro = self.tape[self.count]
        record(**registro)
        self.count += 1


JSONw = [{"ponto": "_MUNDO_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:14:00.885474"},
         {"ponto": "_LINGUA_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:14:01.885474"},
         {"ponto": "_CHAVES_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:14:02.885474"},
         {"ponto": "_MUNDO_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:14:03.885474"},
         {"ponto": "_Mundo_", "valor": "True", "move": "ok", "carta": "28", "casa": "212_448",
          "tempo": "2016-08-08 23:14:07.950161"},
         {"ponto": "_Mundo_", "valor": "True", "move": "ok", "carta": "20", "casa": "84_512",
          "tempo": "2016-08-08 23:14:13.206754"},
         {"ponto": "_Mundo_", "valor": "True", "move": "ok", "carta": "20", "casa": "84_448",
          "tempo": "2016-08-08 23:14:16.513960"},
         {"ponto": "_Mundo_", "valor": "True", "move": "ok", "carta": "19", "casa": "340_512",
          "tempo": "2016-08-08 23:14:20.694364"},
         {"ponto": "_Mundo_", "valor": "True", "move": "ok", "carta": "12", "casa": "84_512",
          "tempo": "2016-08-08 23:14:24.511011"},
         {"ponto": "_Mundo_", "valor": "True", "move": "ok", "carta": "16", "casa": "212_576",
          "tempo": "2016-08-08 23:14:34.284432"},
         {"ponto": "_MUNDO_", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:14:37.755668"},
         {"ponto": "_LINGUA_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:14:42.405210"},
         {"ponto": "_FALA_", "valor": "True", "move": "ok", "carta": "12_30_22", "casa": "0_0",
          "tempo": "2016-08-08 23:15:13.868345"},
         {"ponto": "_FALA_", "valor": "True", "move": "ok", "carta": "22_30_16", "casa": "0_0",
          "tempo": "2016-08-08 23:15:16.906352"},
         {"ponto": "_FALA_", "valor": "True", "move": "ok", "carta": "12_30_22", "casa": "0_0",
          "tempo": "2016-08-08 23:15:20.868345"},
         {"ponto": "_FALA_", "valor": "True", "move": "ok", "carta": "22_30_16", "casa": "0_0",
          "tempo": "2016-08-08 23:15:23.906352"},
         {"ponto": "_LINGUA_", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:15:27.740581"},
         {"ponto": "_CHAVES_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:15:30.897392"},
         {"ponto": "_ABAS_", "valor": "minitens", "move": "ok", "carta": "minitens", "casa": "80_480",
          "tempo": "2016-08-08 23:15:35.086875"},
         {"ponto": "_Chaves_", "valor": "True", "move": "ok", "carta": "12", "casa": "420_340",
          "tempo": "2016-08-08 23:15:37.302902"},
         {"ponto": "_ABAS_", "valor": "minitens", "move": "ok", "carta": "minitens", "casa": "240_480",
          "tempo": "2016-08-08 23:15:38.508119"},
         {"ponto": "_Chaves_", "valor": "True", "move": "ok", "carta": "22", "casa": "520_430",
          "tempo": "2016-08-08 23:15:40.536239"},
         {"ponto": "_ABAS_", "valor": "minitens", "move": "ok", "carta": "minitens", "casa": "400_480",
          "tempo": "2016-08-08 23:15:41.941101"},
         {"ponto": "_Chaves_", "valor": "True", "move": "ok", "carta": "5", "casa": "520_340",
          "tempo": "2016-08-08 23:15:45.837013"},
         {"ponto": "_ABAS_", "valor": "minitens", "move": "ok", "carta": "minitens", "casa": "560_480",
          "tempo": "2016-08-08 23:15:52.815985"},
         {"ponto": "_Chaves_", "valor": "True", "move": "ok", "carta": "17", "casa": "520_250",
          "tempo": "2016-08-08 23:16:04.339382"},
         {"ponto": "_CHAVES_", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-08 23:16:07.585076"}]
JSONX = [{"ponto": "homem", "valor": "True", "move": "ok", "carta": "0", "casa": "0_0",
          "tempo": "2016-08-06 23:59:20.885015"},
         {"ponto": "_MUNDO_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-06 23:59:20.935316"},
         {"ponto": "homem", "valor": "False", "move": "ok", "carta": "0", "casa": "0_0",
          "tempo": "2016-08-06 23:59:22.244403"},
         {"ponto": "_MUNDO_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-06 23:59:22.278820"},
         {"ponto": "_CHAVES_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-06 23:59:24.477236"},
         {"ponto": "_ABAS_", "valor": "objeto", "move": "ok", "carta": "f_r_u_t_a", "casa": "80_500",
          "tempo": "2016-08-06 23:59:29.529234"},
         {"ponto": "_CHAVES_", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-06 23:59:39.856007"},
         {"ponto": "_CHAVES_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-06 23:59:40.483789"},
         {"ponto": "_ABAS_", "valor": "objeto", "move": "ok", "carta": "o_b_j_e_t_o", "casa": "80_500",
          "tempo": "2016-08-06 23:59:44.001565"},
         {"ponto": "_CHAVES_", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-06 23:59:50.636140"},
         {"ponto": "_LINGUA_", "valor": "True", "move": "ok", "carta": "0", "casa": "0_0",
          "tempo": "2016-08-06 23:59:52.275853"},
         {"ponto": "_FALA_", "valor": "True", "move": "ok", "carta": "28_14_70", "casa": "0_0",
          "tempo": "2016-08-06 23:59:54.296230"},
         {"ponto": "_FALA_", "valor": "False", "move": "ok", "carta": "28_14_68", "casa": "0_0",
          "tempo": "2016-08-06 23:59:58.797235"},
         {"ponto": "_FALA_", "valor": "True", "move": "ok", "carta": "28_14_71", "casa": "0_0",
          "tempo": "2016-08-07 00:00:05.938717"},
         {"ponto": "_FALA_", "valor": "True", "move": "ok", "carta": "28_16_71", "casa": "0_0",
          "tempo": "2016-08-07 00:00:17.650000"},
         {"ponto": "_LINGUA_", "valor": "False", "move": "ok", "carta": "0", "casa": "0_0",
          "tempo": "2016-08-07 00:00:23.626584"},
         {"ponto": "homem", "valor": "True", "move": "ok", "carta": "0", "casa": "0_0",
          "tempo": "2016-08-07 00:00:25.440501"},
         {"ponto": "_MUNDO_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-07 00:00:25.472163"},
         {"ponto": "homem", "valor": "False", "move": "ok", "carta": "0", "casa": "0_0",
          "tempo": "2016-08-07 00:00:44.128503"},
         {"ponto": "_MUNDO_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
          "tempo": "2016-08-07 00:00:44.160100"}]
JSON = [{"ponto": "_MUNDO_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
         "tempo": "2016-08-10 14:19:36.630334"},
        {"ponto": "_LINGUA_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
         "tempo": "2016-08-10 14:19:37.630334"},
        {"ponto": "_CHAVES_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
         "tempo": "2016-08-10 14:19:38.630334"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:19:39.630334"},
        {"casa": "520_340", "valor": "True", "move": "ok", "carta": "6", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:19:46.240845"},
        {"casa": "520_250", "valor": "True", "move": "ok", "carta": "6", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:19:51.047479"},
        {"casa": "620_250", "valor": "True", "move": "ok", "carta": "6", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:19:52.699504"},
        {"casa": "620_340", "valor": "True", "move": "ok", "carta": "6", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:19:54.104240"},
        {"casa": "520_250", "valor": "True", "move": "ok", "carta": "6", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:19:56.893084"},
        {"casa": "620_250", "valor": "True", "move": "ok", "carta": "6", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:00.360709"},
        {"casa": "420_160", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:04.448525"},
        {"casa": "420_250", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:06.996789"},
        {"casa": "420_340", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:09.801269"},
        {"casa": "420_430", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:11.941971"},
        {"casa": "520_430", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:15.401573"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_MUNDO_",
         "tempo": "2016-08-10 14:20:15.714751"},
        {"casa": "620_430", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:17.981032"},
        {"casa": "720_430", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:21.953985"},
        {"casa": "720_340", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:24.016742"},
        {"casa": "520_160", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:26.297920"},
        {"casa": "620_160", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:29.362053"},
        {"casa": "340_384", "valor": "True", "move": "ok", "carta": "30", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:20:31.497513"},
        {"casa": "720_250", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:33.458199"},
        {"casa": "0_0", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_MUNDO_",
         "tempo": "2016-08-10 14:20:36.357570"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_MUNDO_",
         "tempo": "2016-08-10 14:20:37.118198"},
        {"casa": "720_160", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:20:37.353182"},
        {"casa": "0_0", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_MUNDO_",
         "tempo": "2016-08-10 14:20:38.128882"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_MUNDO_",
         "tempo": "2016-08-10 14:20:38.717164"},
        {"casa": "0_0", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:20:43.583169"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:20:44.487640"},
        {"casa": "0_0", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:20:45.161836"},
        {"casa": "404_448", "valor": "True", "move": "ok", "carta": "28", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:20:45.422009"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "28", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:20:50.036027"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_LINGUA_",
         "tempo": "2016-08-10 14:20:50.279766"},
        {"casa": "0_0", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_MUNDO_",
         "tempo": "2016-08-10 14:20:51.754532"},
        {"casa": "404_448", "valor": "True", "move": "ok", "carta": "28", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:20:53.554817"},
        {"casa": "404_448", "valor": "True", "move": "ok", "carta": "28", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:20:55.555193"},
        {"casa": "404_448", "valor": "True", "move": "ok", "carta": "28", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:20:56.258987"},
        {"casa": "404_448", "valor": "True", "move": "ok", "carta": "28", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:20:56.785953"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_MUNDO_",
         "tempo": "2016-08-10 14:20:58.420507"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:07.875377"},
        {"casa": "0_0", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_MUNDO_",
         "tempo": "2016-08-10 14:21:10.137219"},
        {"casa": "596_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:13.636005"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:16.715223"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:17.445018"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:17.918100"},
        {"casa": "340_384", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:20.014437"},
        {"casa": "340_384", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:21.036065"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:21.555588"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:22.511151"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:23.115363"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:23.735184"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:23.964238"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:24.355165"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:24.596569"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:24.824615"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:25.054751"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:25.296122"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:25.546890"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:26.736099"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:27.281217"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:27.836735"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:29.035484"},
        {"casa": "404_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:29.816093"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:30.048558"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:30.298394"},
        {"casa": "404_384", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:30.617881"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:31.318344"},
        {"casa": "468_448", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:21:31.575020"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:31.896719"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_47_46", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:21:32.155442"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:21:33.535666"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_LINGUA_",
         "tempo": "2016-08-10 14:21:38.757508"},
        {"casa": "520_340", "valor": "True", "move": "ok", "carta": "7", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:21:39.998060"},
        {"casa": "620_340", "valor": "True", "move": "ok", "carta": "7", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:21:40.735627"},
        {"casa": "520_340", "valor": "True", "move": "ok", "carta": "3", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:21:43.795189"},
        {"casa": "0_0", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:21:47.116377"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:22:07.882252"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "42_44_43", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:09.476243"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "42_44_43", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:10.716711"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "42_44_43", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:11.478811"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "42_44_43", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:12.627092"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "42_44_43", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:13.268482"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "42_44_43", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:14.391551"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "42_44_43", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:14.716844"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "42_44_43", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:15.006238"},
        {"casa": "520_340", "valor": "True", "move": "ok", "carta": "1", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:22:16.492480"},
        {"casa": "620_340", "valor": "True", "move": "ok", "carta": "5", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:22:18.898361"},
        {"casa": "0_0", "valor": "False", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:22:19.828082"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_31_16", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:24.445684"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_31_16", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:25.169376"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "3_31_16", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:22:25.399099"},
        {"casa": "148_384", "valor": "True", "move": "ok", "carta": "22", "ponto": "_Mundo_",
         "tempo": "2016-08-10 14:22:47.030672"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "ponto": "_CHAVES_",
         "tempo": "2016-08-10 14:22:55.969350"},
        {"casa": "420_340", "valor": "True", "move": "ok", "carta": "7", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:22:59.130307"},
        {"casa": "520_340", "valor": "True", "move": "ok", "carta": "0", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:23:01.892471"},
        {"casa": "620_340", "valor": "True", "move": "ok", "carta": "4", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:23:04.628879"},
        {"casa": "720_340", "valor": "True", "move": "ok", "carta": "6", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:23:07.185036"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "39_39_39", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:23:09.124671"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "39_39_39", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:23:09.726388"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "39_39_39", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:23:13.817713"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "39_39_39", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:23:15.185731"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "39_39_39", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:23:15.817739"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "39_39_8", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:23:36.018515"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "39_39_8", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:23:36.696354"},
        {"casa": "520_430", "valor": "True", "move": "ok", "carta": "7", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:23:39.056295"},
        {"casa": "620_430", "valor": "True", "move": "ok", "carta": "7", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:23:41.215662"},
        {"casa": "0_0", "valor": "True", "move": "ok", "carta": "39_39_8", "ponto": "_FALA_",
         "tempo": "2016-08-10 14:23:41.454806"},
        {"casa": "520_250", "valor": "True", "move": "ok", "carta": "7", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:23:43.687648"},
        {"casa": "620_250", "valor": "True", "move": "ok", "carta": "7", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:23:46.398875"},
        {"casa": "420_250", "valor": "True", "move": "ok", "carta": "4", "ponto": "_Chaves_",
         "tempo": "2016-08-10 14:23:51.995644"}]
