from braser.vitollino import Actor
from random import random
from .inventario import MonoInventario, Tabuleiro
from . import Ponto, Folha
from .eica import Jogo, Botao, Imagem

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"


class Null:
    def add(self, _=0):
        pass
NULL = Null()


class Mundo(Jogo):
    """Essa  é a classe Mundo que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self, x):
        super().__init__(ver=False)  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.roda = self.chaves = None
        self.tabuleiro = Tabuleiro(Folha.coisa.n, Ponto(123, 8), Ponto(0, 300-128), Ponto(64, 64), jogo="_Mundo_")
        self.balao = Imagem(Folha.nuvem, Ponto(x+250, -120), self, (3.0, 3.6), ver=False)
        self.inventario = MonoInventario(self.recebe, Ponto(x+300, 45))

    def ativa(self, item=None):
        super().ativa(item)
        self.inventario.ativa(self.ativo)
        self.tabuleiro.ativa(item)
        self.balao.botao.visible = self.ativo
        self.grupo_de_elementos.visible = True
        self.score(evento=Ponto(x=0, y=0), carta="_ATIVA_", ponto="_MUNDO_", valor=self.ativo)

    def recebe(self, item):
        pass
        self.tabuleiro.seleto = item
        self.grupo_de_elementos.add(item)

    def preload(self):
        """Aqui no preload carregamos as imagens de ladrilhos dos items usados no jogo"""
        self.spritesheet(*Folha.coisa.all())
        self.spritesheet(*Folha.animal.all())

    def take_propics(self):
        """o hominídeo tenta retirar uma pedra de grande porte do lugar, 
        observa o cajado e utiliza ele como uma alavanca para deslocar a pedra."""
        pedra = Take(Folha.coisa.n, 16 * 15 - 1, 220, 320)
        cajado = Take(Folha.coisa.n, 16 * 3 + 5, 240, 380, lambda: pedra.activate(pedra.rola), 250, 300)
        cajado.act = cajado.pega


class Take(Actor):
    """Essa  é a classe Take que controla os personagens do jogo"""

    def __init__(self, nome, frame, x, y, effect=lambda: None, hx=0, hy=0):
        super().__init__()
        self.nome, self.frame, self.x, self.y = nome, frame, x, y
        self.homemx, self.homemy = hx, hy
        self.coisa = None
        self.play = 0
        self.act = self.treme
        self.effect = effect

    def create(self):
        """Aqui selecionamos o frame das coisas criadas pela função Take"""
        coisa = self.coisa = self.sprite(self.nome, self.x, self.y)
        coisa.inputEnabled = True
        coisa.input.useHandCursor = True
        coisa.events.onInputDown.add(self._click, self)
        coisa.anchor.setTo(0.5, 0.5)
        coisa.frame = self.frame
        # homem.scale.setTo(0.4, 0.4)

    def activate(self, action=lambda: None):
        self.act = action

    def _click(self, _=None, __=None):
        print("action", _, __)
        self.play = 1
        self.effect()

    """Aqui estão as ações disponíveis para as coisas dos Takes"""

    def treme(self):
        if self.play:
            self.tween(self.coisa, 100, repeat=4, yoyo=True, x=self.coisa.x + 10)
            self.play -= 1

    def rola(self):
        if self.play:
            self.tween(self.coisa, 500, repeat=0, angle=self.coisa.angle - 720, x=self.coisa.x - 40)
            self.play -= 1

    def pega(self):
        if self.play:
            self.tween(self.coisa, 800, repeat=0, x=self.homemx + 2, y=self.homemy + 20, angle=self.coisa.angle + 90)
            self.play -= 1

    def update(self):
        self.act()
