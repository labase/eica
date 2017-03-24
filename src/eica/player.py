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
from browser import timer
from braser.vitollino import Vitollino


class Ativadora:
    def __init__(self, evento, carta, ponto, valor=True):
        self.evento, self.carta, self.ponto, self.valor, = evento, carta, ponto, valor

    def play(self, time, carta=None):
        self.carta = carta if carta else self.carta
        timer.set_timeout(self._play, time)

    def _play(self):
        self.evento()


class Fachada:
    def __init__(self):
        Vitollino.registry = self.registrar
        self.ativadores = {}

    def registrar(self, _, evento, carta, ponto, *args):
        self.ativadores[(ponto, carta)] = Ativadora(evento=evento, carta=carta, ponto=ponto)


JSON = [{"ponto": "_MUNDO_", "valor": "True", "move": "ok", "carta": "__A_T_I_V_A__", "casa": "0_0",
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
