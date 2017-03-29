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

"""Game of Logical Keys, represents the mathematical ontology dimension.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from . import Ponto, Folha
from .inventario import Inventario, Tabuleiro, PONTO, POSICAO
from .eica import Jogo, Imagem

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
BALONX, BALONY = 0, 70
TABUAX, TABUAY, TABUAS = 400, 120, 90


class Chaves(Jogo):
    """Essa  é a classe Chaves que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self, x=BALONX, y=BALONY):
        super().__init__(ver=False)  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.aba_corrente = self.aba = None
        Imagem(Folha.eica, Ponto(-900, -600), self, (2.8, 2.8))
        Imagem(Folha.chaves, Ponto(x+100, y+40), dono=self, escala=(0.9, 0.9))
        self.tabuleiro = Tabuleiro(Folha.coisa.n, posicao=Ponto(POSICAO.x+x, POSICAO.y-80+y), desenha=self.desenha)
        self.inventario = Inventario(self.recebe, Ponto(PONTO.x+x, PONTO.y+y), janela=12)
        self.seleto = None
        self.itens = []

    def desenha(self, carta=(0, ), casa=(100, 100)):
        celula = self.sprite(Folha.minitens.n, casa[0], casa[1])
        celula.frame = carta[0]
        celula.visible = True
        self.recebe(celula)

    def recebe(self, item):
        self.tabuleiro.seleto = item
        self.grupo_de_elementos.add(item)
        self.itens.append(item)

    def ativa(self, ativo=None):
        """Abre o balão de conversa"""
        super().ativa(ativo)
        self.score(evento=Ponto(x=0, y=0), carta="_ATIVA_", ponto="_CHAVES_", valor=self.ativo)
        # self.tween(self.fala, 2000, repeat=0, alpha=1)
        while self.itens:
            self.itens.pop().destroy()
        self.tabuleiro.ativa(self.ativo)
        self.inventario.ativa(self.ativo)

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.image(*Folha.chave.img())
        self.spritesheet(*Folha.coisa.all())
