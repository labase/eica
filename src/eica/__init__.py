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
import os
__version__ = "2.1.2"

here = os.path.dirname(__file__)
IMG = "https://s19.postimg.cc/"
LOCAL = os.path.join(here, "../assets/")


class Ponto:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __repr__(self):
        return self.x, self.y


class Recurso:    
    def __init__(self, n, y, dx=0., dy=0., size=0):
        self.n, self.recurso, self.dx, self.dy, self.size = n, y, dx, dy, size

    def __repr__(self):
        return self.n

    def all(self):
        return self.n, self.recurso, self.dx, self.dy, self.size

    def img(self):
        return self.n, self.recurso


class Folha:
    chaves = Recurso("chaves", LOCAL + "tabela_chaves.png")
    nuvem = Recurso("nuvem", LOCAL + "nuvem.png")
    cumulus = Recurso("cumulus", LOCAL + "cumulus.png")
    twosapiens = Recurso("twosapiens", LOCAL + "dialogo_bg.png", 260, 300, 3)
    sapiens = Recurso("sapiens", LOCAL + "homem01.png")
    itens = Recurso("itens", LOCAL + "spritesheet.png", 200, 200, 6 * 7)
    minitens = Recurso("minitens", LOCAL + "spritesheety.png", 64, 64, 6 * 8)
    coisa = Recurso("objeto", IMG + "vymffyr6b/cacarecos.png", 32, 32, 16 * 16)
    comida = Recurso("objeto", IMG + "vymffyr6b/cacarecos.png", 32, 32, 16 * 16)
    arma = Recurso("objeto", IMG + "vymffyr6b/cacarecos.png", 32, 32, 16 * 16)
    objeto = Recurso("objeto", IMG + "vymffyr6b/cacarecos.png", 32, 32, 16 * 16)
    fruta = Recurso("fruta", IMG + "dllu5egpf/fruit.png", 65, 65, 8 * 8)
    animal = Recurso("animal", IMG + "sk48ztvrj/largeemoji.png", 47.5, 47, 14 * 9)
    arvore = Recurso("arvore", IMG + "v3zvtxjbn/treesprites1.png", 123.5, 111, 4 * 3)
    homem = Recurso("homem", IMG + "88wzr9ssv/caveman.png", 130, 130, 5 * 2)
    fala = Recurso("chave", IMG + "6ek59j5sf/balooni.png")
    chave = Recurso("fala", IMG + "v062dodu7/jogo_chaves.jpg")
    mundo = Recurso("pensa", IMG + "h91lbgowf/thought.png")
    eica = Recurso("fundo", LOCAL + "background.png")
    # eica = Recurso("fundo", IMG + "eicamundo.png")

    @classmethod
    def all(cls):
        return Folha.coisa, Folha.fruta, Folha.animal, Folha.arvore

    @classmethod
    def allThing(cls):
        return [Folha.minitens]*5

    @classmethod
    def alloldThing(cls):
        return Folha.fruta, Folha.comida, Folha.animal, Folha.arma, Folha.objeto
