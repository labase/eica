# from enum import Enum     # for enum34, or the stdlib version
# from aenum import Enum  # for the aenum version
import os
__version__ = "2.0.3"

here = os.path.dirname(__file__)
IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
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
    nuvem = Recurso("nuvem", LOCAL + "nuvem.png")
    cumulus = Recurso("cumulus", LOCAL + "cumulus.png")
    twosapiens = Recurso("twosapiens", LOCAL + "dialogo_bg.png", 260, 300, 3)
    sapiens = Recurso("sapiens", LOCAL + "homem01.png")
    itens = Recurso("itens", LOCAL + "spritesheet.png", 200, 200, 6 * 7)
    minitens = Recurso("minitens", LOCAL + "spritesheety.png", 64, 64, 6 * 7)
    coisa = Recurso("objeto", IMG + "cacarecos.png", 32, 32, 16 * 16)
    comida = Recurso("objeto", IMG + "cacarecos.png", 32, 32, 16 * 16)
    arma = Recurso("objeto", IMG + "cacarecos.png", 32, 32, 16 * 16)
    objeto = Recurso("objeto", IMG + "cacarecos.png", 32, 32, 16 * 16)
    fruta = Recurso("fruta", IMG + "fruit.png", 65, 65, 8 * 8)
    animal = Recurso("animal", IMG + "largeemoji.png", 47.5, 47, 14 * 9)
    arvore = Recurso("arvore", IMG + "treesprites1.png", 123.5, 111, 4 * 3)
    homem = Recurso("homem", IMG + "caveman.png", 130, 130, 5 * 2)
    fala = Recurso("chave", IMG + "balooni.png")
    chave = Recurso("fala", IMG + "jogo_chaves.jpg")
    mundo = Recurso("pensa", IMG + "thought.png")
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
