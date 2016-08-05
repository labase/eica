# -*- coding: UTF8 -*-
from braser.vitollino import Vitollino, Actor

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


class Aba(Elemento):
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
        # self.score(evento=Ponto(x=self.x, y=self.y), carta=chave.aba_corrente.nome, ponto="_ABAS_", valor=proxima.nome)
        chave.aba_corrente = proxima


class Inventario(Elemento):
    """Representa um inventario do jogo"""
    def __init__(self, recebe, nome, frame, x, y):
        super().__init__()
        self.recebe, self.nome, self.frame, self.x, self.y = recebe, nome, frame, x, y
        self.aba = self.coisas = self.aba_corrente = None
        self.seleto = None
        self.fruta = self.animal = self.comida = None
        self.arvore = self.arma = self.objeto = None
        self.x, self.y = x, y
        self.monta_abas()
        self.abas = [self.fruta, self.animal, self.comida, self.arma, self.objeto,
                     self.fruta, self.animal, self.comida, self.arma, self.objeto]

        self.ladrilho_coisa = "objeto"
        self.ladrilho_fruta = "fruta"
        self.ladrilho_animal = "animal"
        self.ladrilho_arvore = "arvore"
        self.ladrilho_fala = "chave"

    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.spritesheet(self.ladrilho_fruta, IMG + "fruit.png", 65, 65, 8 * 8)
        self.spritesheet(self.ladrilho_animal, IMG + "largeemoji.png", 47.5, 47, 14 * 9)
        self.spritesheet(self.ladrilho_coisa, IMG + "cacarecos.png", 32, 32, 16 * 16)
        self.spritesheet(self.ladrilho_arvore, IMG + "treesprites1.png", 123.5, 111, 4 * 3)

    def monta_abas(self):
        """Jogador escreve: hominídeo comer fruta_vermelha."""
        self.fruta = Item(self.recebe, self.ladrilho_fruta, 0, self.x + FALAX, self.y + FALAY)
        self.animal = Item(self.recebe, self.ladrilho_animal, 4 * 14 + 7, self.x + FALAX, self.y + FALAY)
        self.comida = Item(self.recebe, self.ladrilho_coisa, 5 * 16 + 6, self.x + FALAX, self.y + FALAY)
        # self.arvore = Item(self.recebe, self.ladrilho_arvore, 0, self.x+FALAX+FALASEPARA*2, self.y+FALAY)
        self.arma = Item(self.recebe, self.ladrilho_coisa, 16 * 4, self.x + FALAX, self.y + FALAY)
        self.objeto = Item(self.recebe, self.ladrilho_coisa, 16 + 7, self.x + FALAX, self.y + FALAY)
        self.aba_corrente = self.fruta

    def mostra_abas(self, corrente, proxima):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        print("mostra_abas", proxima.nome)
        corrente.mostra(False)
        proxima.mostra(True)

        self.aba_corrente = proxima

    def ativa(self):
        """Abre o balão de conversa"""
        # self.tween(self.fala, 2000, repeat=0, alpha=1)
        for aba in self.abas:
            aba.mostra(False)
        self.aba_corrente.mostra(self.ativo)

    def cria_abas(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        for x in range(10):
            Aba(self, self.abas[x], FALAX - ABAS + x * ABAS, FALAY - 50)

    def mostra(self, muda):
        """ Mostra esta aba

        :param muda: booleano que diz se é para mostar ou chavesocultar a aba
        :return: None
        """
        self.aba.visible = muda


class Item(Elemento):
    """Representa um Item do jogo"""
    def __init__(self, recebe, nome, frame, x, y):
        super().__init__()
        self.recebe, self.nome, self.frame, self.x, self.y = recebe, nome, frame, x, y
        self.aba = self.coisas = None
        self.seleto = None

    def mostra(self, muda):
        """ Mostra esta aba

        :param muda: booleano que diz se é para mostar ou ocultar a aba
        :return: None
        """
        self.aba.visible = muda

    def rola(self, desloca):
        """Aqui rolamos o conjunto de sprites mudando o frame de cada sprite"""
        self.frame = self.frame + desloca if self.frame + desloca > 0 else 0
        for frame, coisa in enumerate(self.coisas):
            print(frame, coisa.frame)
            coisa.frame = self.frame + frame

    def create(self):
        """Cria uma aba que contem todos elementos do inventário"""
        self.aba = self.group()
        self.aba.visible = False
        self.coisas = [self._create(coisa) for coisa in range(0, 8)]

    def _create(self, frame):
        """Aqui colocamos o sprite do icon e adicionamos chavesno seletor de aba"""
        coisa = self._copy(frame)
        self.aba.add(coisa)
        # self.recebe.jogo.add(coisa)
        return coisa

    def _copy(self, frame):
        """Aqui colocamos o sprite do icon e selecionamos o frame que o representa"""
        coisa = self.sprite(self.nome, self.x + 50 * frame, self.y)
        coisa.frame = self.frame + frame
        coisa.inputEnabled = True
        coisa.input.useHandCursor = True
        coisa.events.onInputDown.add(lambda _=None, b=frame, c=frame: self._click(b, c), dict(b=frame))
        coisa.anchor.setTo(0.5, 0.5)
        return coisa

    def activate(self):
        self.aba.visible = True

    def _click(self, _=None, d=None):
        """ Seleciona o ícone que vai mover

        :param d:
        :return:
        """
        print("action", d)
        self.seleto = self._copy(d)
        self.recebe(self.seleto)
