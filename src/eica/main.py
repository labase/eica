from braser.vitollino import Vitollino, Actor
from .mundo import Mundo
from .roda import Roda
from .chaves import Chaves

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"

class Jogo(Vitollino):
    JOGO = None
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""
    def __init__(self, gid):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.ladrilho_homem = "homem"
        self.set_id(gid)
        self.homem = Homem(self.ladrilho_homem, 2, 250, 300)
        self.mundo = Mundo()
        self.roda = Roda()
        self.chaves = Chaves()
        self.mundo.roda = self.roda
        self.mundo.chaves = self.chaves

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.image("fundo", IMG + "eicamundo.png")
        self.spritesheet(self.ladrilho_homem, IMG + "caveman.png", 130, 130, 5*2)

    def create(self):
        """Aqui colocamos a imagem do mundo na tela do jogo"""
        fundo = self.sprite("fundo")
        fundo.scale.setTo(1.6, 1.6)
        # fundo.resizeWorld()


class Homem(Actor):
    """Essa  é a classe Homem que controla os personagens do jogo"""
    def __init__(self, nome, frame, x, y):
        super().__init__()
        self.nome, self.frame, self.x, self.y = nome, frame, x, y
        self.homem = None

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        homem = self.homem = self.sprite(self.nome, self.x, self.y)
        homem.frame = self.frame
        homem.scale.setTo(0.4, 0.4)
        homem.events.onInputDown.add(self._click, self)

    def _click(self, _=None, __=None):
        """Ativa o jogo da Roda"""
        print("homem action")
        Jogo.JOGO.roda.ativa()


def main(gid=None):
    Jogo.JOGO = Jogo(gid)

if __name__ == "__main__":
    main()
