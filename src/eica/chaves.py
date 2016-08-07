from braser.vitollino import Actor
from . import Ponto
from .inventario import Inventario, Tabuleiro

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
BALONX, BALONY = 0, 70
TABUAX, TABUAY, TABUAS = 400, 120, 90


class Chaves(Actor):
    """Essa  é a classe Chaves que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self, x=BALONX, y=BALONY):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.aba_corrente = self.aba = None
        # self.abas = "fruta objeto animal arma"
        self.ladrilho_coisa = "objeto"
        self.ladrilho_fruta = "fruta"
        self.ladrilho_animal = "animal"
        self.ladrilho_arvore = "arvore"
        self.ladrilho_fala = "chave"
        self.fala = self.falou = self.pensa = None
        self.x, self.y = x, y
        self.jogo = None
        self.tabuleiro = Tabuleiro(self.ladrilho_coisa)
        # self.cria_tabuleiro()
        # self.take_propils()
        self.inventario = Inventario(self.recebe)
        self.ativo = True
        self.seleto = None

    def recebe(self, item):
        self.tabuleiro.seleto = item
        self.jogo.add(item)

    def ativa(self):
        """Abre o balão de conversa"""
        self.score(evento=Ponto(x=0, y=0), carta="_ATIVA_", ponto="_CHAVES_", valor=self.ativo)
        self.jogo.visible = self.ativo
        # self.tween(self.fala, 2000, repeat=0, alpha=1)
        self.tabuleiro.ativa(self.ativo)
        self.inventario.ativa(self.ativo)
        self.ativo = not self.ativo

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.image(self.ladrilho_fala, IMG + "jogo_chaves.jpg")

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        self.fala = self.sprite(self.ladrilho_fala, self.x, self.y)
        self.jogo = self.group()
        self.fala.scale.setTo(2, 2)
        self.jogo.add(self.fala)
        self.jogo.visible = False
        # self.tabuleiro.ativa(False)
