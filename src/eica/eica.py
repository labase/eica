# -*- coding: UTF8 -*-
from braser.vitollino import Vitollino, Actor
from . import Ponto

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
BALONX, BALONY = 0, 70
TABUAX, TABUAY, TABUAS = 400, 120, 90
FALAX, FALAY, FALASEPARA = 100, 550, 100
ABAS = 80


class Eica(Vitollino):
    JOGO = None
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""
    def __init__(self, gid):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.ladrilho_homem = "homem"
        self.set_id(gid)

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.image("fundo", IMG + "eicamundo.png")
        self.spritesheet(self.ladrilho_homem, IMG + "caveman.png", 130, 130, 5*2)

    def create(self):
        """Aqui colocamos a imagem do mundo na tela do jogo"""
        fundo = self.sprite("fundo")
        fundo.scale.setTo(1.6, 1.6)


class Elemento(Actor):
    """Representa elementos do jogo"""
    def __init__(self):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus

    def preload(self):
        """Aqui no preload carregamos as folhas de ladrilho"""
        pass

    def create(self):
        """Aqui colocamos as imagems na tela do jogo"""
        pass

    def update(self):
        """A engenharia do jogo é feita aqui"""
        pass


class Jogo(Elemento):
    """Essa  é a classe Mundo que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.ativo = False
        self.ladrilho = "_%s_" % str(self.__name__)
        self.grupo_de_elementos = None

    def ativa(self):
        """Abre o balão de conversa"""
        self.ativo = not self.ativo
        self.grupo_de_elementos.visible = self.ativo
        self.score(evento=Ponto(x=0, y=0), carta="0", ponto=self.ladrilho, valor=self.ativo)
