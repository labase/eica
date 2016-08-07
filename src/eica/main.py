from braser.vitollino import Vitollino, Actor
from .mundo import Mundo
from .roda import Roda
from .chaves import Chaves
from .eica import Jogo, Imagem, Botao
from .inventario import Inventario, MonoInventario
from . import Folha, Ponto

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"


class MiniEica(Vitollino):
    JOGO = None
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self, gid):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        Eica()


class Eica(Jogo):
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        Imagem(Folha.eica, Ponto(0, 0), self, (1.6, 1.6))
        Homem(self.clica)
        self.mundo = MonoInventario(lambda _=0: None)

    def clica(self, item):
        """Aqui colocamos as imagems na tela do jogo"""
        self.mundo.ativa(True or self.ativo)
        # self.ativa()


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

    def __init__(self, acao=None, frame=2, x=250, y=300):
        super().__init__()
        acao = acao or self._click
        # Imagem(Folha.eica, Ponto(0, 0), self, (1.6, 1.6))
        Botao(Folha.homem, Ponto(x=250, y=300), frame, acao, self, (0.4, 0.4))

    def _click(self, _=None, __=None):
        """Ativa o jogo do Mundo"""
        print("homem action", JogoEica.JOGO.mundo)
        self.ativa()
        JogoEica.JOGO.mundo.ativa()


def main(gid=None):
    JogoEica.JOGO = JogoEica(gid)
    # JogoEica.JOGO = MiniEica(gid)


if __name__ == "__main__":
    main()
