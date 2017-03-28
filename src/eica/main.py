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

"""Main defines the scenes and the homo sapiens character, the actor of EICA game.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""

from braser.vitollino import Vitollino, Actor
from .mundo import Mundo
from .roda import Roda
from .chaves import Chaves
from .eica import Jogo, Imagem, Botao
from .inventario import Inventario, MonoInventario
from . import Folha, Ponto, __version__


class JogoEica(Vitollino):
    JOGO = None
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self, gid, w=1000, h=800):
        super().__init__(w, h, alpha=True)  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.eica = Eica()


class Menu(Jogo):
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self, jogo):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        Botao(Folha.itens, Ponto(15, 15), 36 + 1, lambda i: jogo.ativaroda(i), self, escala=(0.6, 0.6))
        Botao(Folha.itens, Ponto(735+50, 15), 36 + 3, lambda i: jogo.ativachaves(i), self, escala=(0.6, 0.6))


class Eica(Jogo):
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        Imagem(Folha.eica, Ponto(-500, -200), self, (1.8, 1.8))
        ''''''
        self.mundo = Mundo(x=-150)  # MonoInventario(lambda _=0: None)
        self.homem = Homem(lambda i: self.activating(i))
        self.roda = Roda(acao=self.homem.esconde)
        self.chaves = Chaves(y=100)
        self.menu = Menu(self)

    def activating(self, *_):
        self.register(evento=self.activating, carta="_ATIVA_", ponto="_MUNDO_", valor=True)
        self.activating = self.clica

    def ativaroda(self, *_):
        self.register(evento=self.ativaroda, carta="_ATIVA_", ponto="_LINGUA_", valor=self.ativo)
        self.ativaroda = self._ativaroda

    def _ativaroda(self, *_):
        self.roda.ativa()

    def ativachaves(self, *_):
        self.register(evento=self.ativachaves, carta="_ATIVA_", ponto="_CHAVES_", valor=self.ativo)
        self.ativachaves = self._ativachaves

    def _ativachaves(self, *_):
        self.chaves.ativa()

    def clica(self, *_):
        """Aqui colocamos as imagems na tela do jogo"""
        print("ativamundo", self.mundo.ativo)
        self.mundo.ativa()
        print("ativamundo", self.mundo.ativo)
        # self.ativa()

    def preload(self):
        """Aqui no preload carregamos as imagens de ladrilhos dos items usados no jogo"""
        self.spritesheet(*Folha.animal.all())
        self.spritesheet(*Folha.itens.all())
        self.spritesheet(*Folha.minitens.all())


class Homem(Jogo):
    """Essa  é a classe Homem que controla os personagens do jogo"""

    def __init__(self, acao=None, frame=2, x=250, y=300):
        super().__init__()
        acao = acao or self._click
        # Imagem(Folha.eica, Ponto(0, 0), self, (1.6, 1.6))
        self.homem = Botao(Folha.sapiens, Ponto(x=250, y=450), frame, lambda i: acao(i), self, (0.1, 0.1))

    def esconde(self, ativa=False):
        """Esconde o Homem"""
        print("homem action Esconde", ativa)
        self.homem.botao.visible = ativa

    def _click(self, *_):
        """Ativa o jogo do Mundo"""
        print("homem action", JogoEica.JOGO.mundo)
        self.ativa()
        JogoEica.JOGO.mundo.ativa(self.ativo)


def main(gid=None):
    # JogoEica.JOGO = JogoEica(gid)
    JogoEica.JOGO = JogoEica(gid)
    return __version__


class MonkeyPatcher:

    def score(self, evento, carta, ponto, valor):
        carta = '_'.join(carta)
        casa = evento
        data = dict(doc_id=Vitollino.GID, carta=carta, casa=casa, move="ok", ponto=ponto, valor=valor)
        print('store', data)


def player(gid=None):
    # JogoEica.JOGO = JogoEica(gid)
    print("player")
    from .player import Fachada, JSON
    fachada = Fachada()
    from braser.vitollino import Vitollino
    Vitollino.score = MonkeyPatcher.score
    # Vitollino.score = lambda *a, **k: None
    jogo = JogoEica.JOGO = JogoEica(gid, 800, 800)
    jogo.eica.mundo.ativo = False
    print(list(fachada.ativadores.keys()))
    fachada.player(tape=JSON, time=20, delta=200)

    return __version__


if __name__ == "__main__":
    main()
