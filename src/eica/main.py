from braser.vitollino import Vitollino, Actor
from .mundo import Mundo

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"

class Jogo(Vitollino):
    """Essa  é a classe Jogo que recebe os poderes da classe Circus de poder criar um jogo"""
    def __init__(self):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.ladrilho_homem = "homem"
        self.homem = Homem(self.ladrilho_homem, 2, 250, 300)
        self.mundo = Mundo()

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


def main(_=None):
    Jogo()

if __name__ == "__main__":
    main()
