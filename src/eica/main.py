from braser.vitollino import Vitollino, Actor
from .mundo import Mundo
from .roda import Roda
from .chaves import Chaves
from .eica import Jogo

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"


class JogoEica(Vitollino):
    JOGO = None
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self, gid):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.ladrilho_homem = "homem"
        self.set_id(gid)
        self.mundo = Mundo()
        self.homem = Homem()
        self.roda = Roda()
        self.chaves = Chaves()
        self.mundo.roda = self.roda
        self.mundo.chaves = self.chaves

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.image("fundo", IMG + "eicamundo.png")
        # self.spritesheet(self.ladrilho_homem, IMG + "caveman.png", 130, 130, 5 * 2)

    def create(self):
        """Aqui colocamos a imagem do mundo na tela do jogo"""
        fundo = self.sprite("fundo")
        fundo.scale.setTo(1.6, 1.6)
        # fundo.resizeWorld()


class Homem(Jogo):
    """Essa  é a classe Homem que controla os personagens do jogo"""

    def __init__(self, frame=2, x=250, y=300):
        super().__init__()
        self.frame, self.x, self.y = frame, x, y
        self.homem = None
        self.pensa = None

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.ladrilho = "_HOMEM_"
        self.image("pensa", IMG + "thought.png")
        # self.spritesheet(self.ladriho, IMG + "caveman.png", 130, 130, 5 * 2)
        self.spritesheet("homem", IMG + "caveman.png", 130, 130, 5 * 2)

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        # pensa = self.pensa = self.sprite("pensa", 200, -10)
        # pensa.scale.setTo(2.1, 1.4)
        self.grupo_de_elementos = self.group()
        # self.grupo_de_elementos.add(pensa)
        self.grupo_de_elementos.visible = False

        print(" Homem(Jogo):", self.ladrilho, self.x, self.y)
        homem = self.homem = self.sprite("homem", self.x, self.y)
        # homem = self.homem = self.sprite(self.ladriho, self.x, self.y)
        homem.frame = self.frame
        homem.inputEnabled = True
        homem.scale.setTo(0.4, 0.4)
        homem.events.onInputDown.add(self._click, self)

    def _click(self, _=None, __=None):
        """Ativa o jogo do Mundo"""
        print("homem action", JogoEica.JOGO.mundo)
        self.ativa()
        JogoEica.JOGO.mundo.ativar(self.ativo)


def main(gid=None):
    JogoEica.JOGO = JogoEica(gid)


if __name__ == "__main__":
    main()
