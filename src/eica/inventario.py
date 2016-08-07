from braser.vitollino import Actor
from . import Ponto
from .eica import Botao
from random import shuffle

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
BALONX, BALONY = 0, 70
TABUAX, TABUAY, TABUAS = 400, 120, 90
FALAX, FALAY, FALASEPARA = 100, 550, 100
ABAS = 80
DIMENSAO = Ponto(4, 4)
POSICAO = Ponto(400, 120)
QUADRICULA = Ponto(100, 90)


class Celula(Actor):
    def __init__(self, recurso, tabuleiro=None, x=BALONX, y=BALONY):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.celula = recurso
        self.x, self.y, self.tabuleiro = x, y, tabuleiro

    def create(self):
        self.celula = self.sprite(self.celula, self.x, self.y)
        # self.celula.scale.setTo(2.5, 2.5)
        self.celula.inputEnabled = True
        self.celula.frame = 160
        self.celula.width, self.celula.height = self.tabuleiro.quadro.x, self.tabuleiro.quadro.y
        self.celula.events.onInputDown.add(lambda _=0, __=0: self.recebe(self.tabuleiro), self)
        self.tabuleiro.tabuleiro.add(self.celula)

    def recebe(self, tabuleiro):
        item = tabuleiro.seleto
        if not item:
            return
        item.x, item.y = self.x + 20, self.y + 20
        self.score(evento=Ponto(x=item.x, y=item.y), carta=[str(item.frame)], ponto=self.tabuleiro.ladrilho, valor=True)


class Tabuleiro(Celula):

    def __init__(self, tab, dimensao=DIMENSAO, posicao=POSICAO, quadro=QUADRICULA, jogo="_Chaves_"):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        super().__init__(tab)  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.ladrilho = jogo
        self.seleto = self.tabuleiro = None
        self.quadro = quadro
        for x in range(dimensao.x):
            for y in range(dimensao.y):
                Celula(tab, self, posicao.x + x * quadro.x, posicao.y + y * quadro.y)

    def create(self):
        self.tabuleiro = self.group()
        self.tabuleiro.visible = False

    def ativa(self, ativa):
        """Abre o balão de conversa"""
        self.tabuleiro.visible = ativa


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
        self.score(evento=Ponto(x=self.x, y=self.y), carta=[chave.aba_corrente.nome], ponto="_ABAS_", valor=proxima.nome)
        chave.aba_corrente = proxima


class Inventario(Actor):
    """Essa  é a classe Chaves que recebe os poderes da classe Circus de poder criar um jogo"""
    preloader = None

    def __init__(self, recebe, x=BALONX, y=BALONY+FALAY, delta=Ponto(750, 0)):
        Inventario.preloader = Inventario.preloader or self._preload
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.aba_corrente = self.aba = None
        self.recebe = recebe
        self.ladrilho_coisa = "objeto"
        self.ladrilho_fruta = "fruta"
        self.ladrilho_animal = "animal"
        self.ladrilho_arvore = "arvore"
        self.ladrilho_fala = "chave"
        self.fala = self.falou = self.pensa = None
        self.fruta = self.animal = self.comida = None
        self.arvore = self.arma = self.objeto = None
        self.x, self.y, self.delta = x, y, delta
        self.jogo = None
        self.monta_abas()
        self.abas = [self.fruta, self.animal, self.comida, self.arma, self.objeto,
                     self.fruta, self.animal, self.comida, self.arma, self.objeto]
        self.cria_abas()
        Botao(self.ladrilho_animal, Ponto(self.x, 2*self.delta.y+self.y-20), 14 * 9 - 4, self.up, self)
        Botao(self.ladrilho_animal, Ponto(self.x + self.delta.x, 2*self.delta.y+self.y-20), 14 * 9 - 5, self.down, self)
        self.ativo = True

    def add(self, item):
        """Abre o balão de conversa"""
        self.jogo.add(item)

    def ativa(self, ativa):
        """Abre o balão de conversa"""
        # self.score(evento=Ponto(x=0, y=0), carta="0", ponto="_CHAVES_", valor=self.ativo)
        self.jogo.visible = ativa
        # self.tween(self.fala, 2000, repeat=0, alpha=1)
        for aba in self.abas:
            aba.mostra(False)
        self.aba_corrente.mostra(ativa)

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        # Inventario.preloader()
        self._preload()

    def _preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.spritesheet(self.ladrilho_fruta, IMG + "fruit.png", 65, 65, 8 * 8)
        self.spritesheet(self.ladrilho_animal, IMG + "largeemoji.png", 47.5, 47, 14 * 9)
        self.spritesheet(self.ladrilho_coisa, IMG + "cacarecos.png", 32, 32, 16 * 16)
        self.spritesheet(self.ladrilho_arvore, IMG + "treesprites1.png", 123.5, 111, 4 * 3)
        Inventario.preloader = lambda _=0: None

    def monta_abas(self):
        """Jogador escreve: hominídeo comer fruta_vermelha."""
        self.fruta = Item(self.recebe, self.ladrilho_fruta, 0, self.x + FALAX, self.y)
        self.animal = Item(self.recebe, self.ladrilho_animal, 4 * 14 + 7, self.x + FALAX, self.y + self.delta.y * 1)
        self.comida = Item(self.recebe, self.ladrilho_coisa, 5 * 16 + 6, self.x + FALAX, self.y + self.delta.y * 2)
        # self.arvore = Item(self.recebe, self.ladrilho_arvore, 0, self.x+FALAX+FALASEPARA*2, self.y+FALAY)
        self.arma = Item(self.recebe, self.ladrilho_coisa, 16 * 4, self.x + FALAX, self.y + self.delta.y * 3)
        self.objeto = Item(self.recebe, self.ladrilho_coisa, 16 + 7, self.x + FALAX, self.y + self.delta.y * 4)
        self.aba_corrente = self.fruta

    def mostra_abas(self, corrente, proxima):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        # print("mostra_abas", proxima.nome)
        corrente.mostra(False)
        proxima.mostra(True)

        self.aba_corrente = proxima

    def cria_abas(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        for x in range(10):
            Aba(self, self.abas[x], self.x - ABAS + x * ABAS, self.y - BALONY - 50)

    def up(self, _=None, __=None):
        self.aba_corrente.rola(-1)

    def down(self, _=None, __=None):
        self.aba_corrente.rola(1)

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        self.jogo = self.jogo or self.group()
        self.jogo.visible = False

        self.aba = self.group()
        self.aba.visible = False


class MonoInventario(Inventario):
    """Essa  é a classe Item que seve tanto como ítem como coleção de itens"""

    def __init__(self, recebe, x=BALONX, y=BALONY):
        super().__init__(recebe, x, y, Ponto(400, 45))  # invocado aqui para preservar os poderes recebidos do Circus
        self.abas = [self.fruta, self.animal, self.comida, self.arma, self.objeto]

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        super().preload()
        self.image("pensa", IMG + "thought.png")

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        pensa = self.pensa = self.sprite("pensa", 200, -10)
        pensa.scale.setTo(2.1, 1.4)
        self.jogo = self.jogo or self.group()
        self.jogo.add(pensa)
        super().create()  # invocado aqui para preservar os poderes recebidos do Circus
        self.jogo.visible = False

    def cria_abas(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        pass

    def ativa(self, ativa):
        """Abre o balão de conversa"""
        print("MonoInventario", ativa)
        self.jogo.visible = ativa
        [aba.mostra(ativa) for aba in self.abas]
        self.score(evento=Ponto(x=0, y=0), carta="_ATIVA_", ponto="_MUNDO_", valor=self.ativo)

    def up(self, _=None, __=None):
        [aba.rola(-1) for aba in self.abas]

    def down(self, _=None, __=None):
        [aba.rola(1) for aba in self.abas]


class Item(Actor):
    """Essa  é a classe Item que seve tanto como ítem como coleção de itens"""

    def __init__(self, recebe, nome, frame, x, y, stepx=50, janela=8):
        super().__init__()
        self.recebe, self.nome, self.frame, self.x, self.y,\
            self.stepx, self.janela = recebe, nome, frame, x, y, stepx, janela
        self.aba = self.coisas = self.fala = self.jogo = None
        self.seleto = None
        self.range = list(range(0, self.janela))

    def mostra(self, muda):
        """ Mostra esta aba

        :param muda: booleano que diz se é para mostar ou ocultar a aba
        :return: None
        """
        self.aba.visible = muda
        shuffle(self.range)
        self.rola(0)

    def rola(self, desloca):
        """Aqui rolamos o conjunto de sprites mudando o frame de cada sprite"""
        # self.frame = self.frame + desloca if self.frame + desloca > 0 else 0
        self.range = (self.range + self.range + self.range)[self.janela+desloca: 2*self.janela+desloca]
        for coisa in self.coisas:
            coisa.visible = False
        for frame, coisa in list(zip(self.range, self.coisas))[:6]:
            # print(frame, coisa.frame)
            coisa.frame = self.frame + frame
            coisa.visible = True

    def create(self):
        """Cria coleção de coisas, a aba como um grupo de sprites e faz a aba ficar invisível"""
        self.aba = self.group()
        self.aba.visible = False
        self.coisas = [self._create(coisa) for coisa in self.range]

    def _create(self, frame):
        """Aqui colocamos o sprite do icon e adicionamos no seletor de aba"""
        coisa = self._copy(frame)
        self.aba.add(coisa)
        return coisa

    def _copy(self, frame):
        """Aqui colocamos o sprite do icon e selecionamos o frame que o representa"""
        coisa = self.sprite(self.nome, self.x + self.stepx * frame, self.y)
        coisa.frame = self.frame + frame
        coisa.inputEnabled = True
        coisa.input.useHandCursor = True
        coisa.events.onInputDown.add(lambda a=None, b=coisa, c=coisa: self._click(b, c), dict(b=coisa))
        coisa.anchor.setTo(0.5, 0.5)
        return coisa

    def _click(self, _=None, item=None):
        """ Seleciona o ícone que vai mover

        :param item:
        :return:
        """
        print("action", item.frame)
        self.seleto = self.sprite(self.nome, 0, -1000)
        self.seleto.frame = item.frame
        self.recebe(self.seleto)

    def update(self):
        pass
