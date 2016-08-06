from braser.vitollino import Actor
from . import Ponto
from .inventario import Inventario

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
BALONX, BALONY = 0, 70
TABUAX, TABUAY, TABUAS = 400, 120, 90
FALAX, FALAY, FALASEPARA = 100, 550, 100
ABAS = 80


class Aba(Actor):
    def __init__(self, chave, tab, x=BALONX, y=BALONY):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.aba = tab
        self.celula = None
        self.chave, self.x, self.y = chave, x, y

    def create(self):
        self.celula = self.sprite(self.chave.ladrilho_coisa, self.x, self.y)
        self.celula.scale.setTo(2.5, 2.5)
        self.celula.inputEnabled = True
        self.celula.frame = 0  # 160
        self.celula.events.onInputDown.add(lambda _=0, __=0: self.mostra_abas(self.chave, self.aba), self)
        self.chave.jogo.add(self.celula)

    def mostra_abas(self, chave, proxima):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        print("mostra_abas", proxima.nome, chave.aba_corrente.nome)
        chave.aba_corrente.mostra(False)
        proxima.mostra(True)
        self.score(evento=Ponto(x=self.x, y=self.y), carta=chave.aba_corrente.nome, ponto="_ABAS_", valor=proxima.nome)
        chave.aba_corrente = proxima


class Celula(Actor):
    def __init__(self, chave, tab, x=BALONX, y=BALONY):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.celula = tab
        self.chave, self.x, self.y = chave, x, y

    def create(self):
        self.celula = self.sprite(self.chave.ladrilho_coisa, self.x, self.y)
        self.celula.scale.setTo(2.5, 2.5)
        self.celula.inputEnabled = True
        self.celula.frame = 160
        self.celula.events.onInputDown.add(lambda _=0, __=0: self.recebe(self.chave.seleto), self)

    def recebe(self, item):
        if not item:
            return
        item.x, item.y = self.x + 40, self.y + 40
        self.score(evento=Ponto(x=item.x, y=item.y), carta="0", ponto="_CHAVE_", valor=item.frame)


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
        self.cria_tabuleiro()
        # self.take_propils()
        self.inventario = Inventario(self.recebe)
        self.ativo = True
        self.seleto = None

    def recebe(self, item):
        self.seleto = item
        self.jogo.add(item)

    def ativa(self):
        """Abre o balão de conversa"""
        self.score(evento=Ponto(x=0, y=0), carta="0", ponto="_CHAVES_", valor=self.ativo)
        self.jogo.visible = self.ativo
        # self.tween(self.fala, 2000, repeat=0, alpha=1)
        self.inventario.ativa(self.ativo)
        self.ativo = not self.ativo

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.image(self.ladrilho_fala, IMG + "jogo_chaves.jpg")

    def mostra_abas(self, corrente, proxima):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        self.inventario.mostra_abas(self, corrente, proxima)

    def cria_tabuleiro(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        for x in range(4):
            for y in range(4):
                pass
                tab = None  # self.sprite(self.ladrilho_coisa, TABUAX + x * TABUAS * 1.1, TABUAY + y * TABUAS)
                Celula(self, tab, TABUAX + x * TABUAS * 1.1, TABUAY + y * TABUAS)

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        self.fala = self.sprite(self.ladrilho_fala, self.x, self.y)
        self.jogo = self.group()
        self.fala.scale.setTo(2, 2)
        self.jogo.add(self.fala)
        self.jogo.visible = False
