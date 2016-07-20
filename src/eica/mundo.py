from braser.vitollino import Actor
from random import random

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"

class Mundo(Actor):
    """Essa  é a classe Mundo que recebe os poderes da classe Circus de poder criar um jogo"""
    def __init__(self):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.ladrilho_coisa = "coisa"
        self.ladrilho_icon = "icon"
        self.roda = self.chaves = None
        self.take_propics()

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.spritesheet(self.ladrilho_coisa, IMG + "cacarecos.png", 32, 32, 16*16)
        self.spritesheet(self.ladrilho_icon, IMG + "largeemoji.png", 47.5, 47, 16*16)

    def create(self):
        """Aqui colocamos o selecionador dos jogos da roda e chaves lógicas"""
        roda = self.sprite(self.ladrilho_icon, 100, 700)
        roda.inputEnabled = True
        roda.input.useHandCursor = True
        roda.events.onInputDown.add(lambda _, __: self.roda.ativa(), self)
        roda.anchor.setTo(0.5, 0.5)
        roda.frame = 3*14+4
        chaves = self.sprite(self.ladrilho_icon, 700, 700)
        chaves.inputEnabled = True
        chaves.input.useHandCursor = True
        chaves.events.onInputDown.add(lambda _, __: self.chaves.ativa(), self)
        chaves.anchor.setTo(0.5, 0.5)
        chaves.frame = 3*14+4
        #homem.scale.setTo(0.4, 0.4)

    def take_propics(self):
        """o hominídeo tenta retirar uma pedra de grande porte do lugar, 
        observa o cajado e utiliza ele como uma alavanca para deslocar a pedra."""
        pedra = Take(self.ladrilho_coisa, 16 * 15 - 1, 220, 320)
        rola = lambda: pedra.activate(pedra.rola)
        cajado = Take(self.ladrilho_coisa, 16 * 3 + 5, 240, 380, rola, 250, 300)
        cajado.act = cajado.pega


class Take(Actor):
    """Essa  é a classe Take que controla os personagens do jogo"""
    def __init__(self, nome, frame, x, y, effect=lambda :None, hx=0, hy=0):
        super().__init__()
        self.nome, self.frame, self.x, self.y = nome, frame, x, y
        self.homemx, self.homemy = hx, hy
        self.coisa = None
        self.play = 0
        self.act = self.treme
        self.effect = effect

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        coisa = self.coisa = self.sprite(self.nome, self.x, self.y)
        coisa.inputEnabled = True
        coisa.input.useHandCursor = True
        coisa.events.onInputDown.add(self._click, self)
        coisa.anchor.setTo(0.5, 0.5)
        coisa.frame = self.frame
        #homem.scale.setTo(0.4, 0.4)

    def activate(self, action=lambda: None):
        self.act = action

    def _click(self, _=None, __=None):
        print("action", _, __)
        self.play = 30
        self.effect()

    def treme(self):
        if self.play:
            self.play -= 1
            self.coisa.position.x += 3 - 6 *random()

    def rola(self):
        if self.play:
            self.play -= 1
            self.coisa.position.x -= 5
            self.coisa.angle -= 30

    def pega(self):
        deltax = (self.homemx - self.coisa.position.x) / 10
        deltay = (self.homemy - self.coisa.position.y) / 10
        if self.play:
            self.play -= 1
            self.coisa.position.x += deltax
            self.coisa.position.y += deltay

    def update(self):
        self.act()

