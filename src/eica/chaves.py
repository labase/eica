from braser.vitollino import Actor
from random import random

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
BALONX, BALONY = 0, 70
TABUAX, TABUAY, TABUAS = 400, 120, 90
FALAX, FALAY, FALASEPARA = 70,40, 100


class Celula(Actor):
    def __init__(self,chave,  tab, x=BALONX, y=BALONY):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.celula = tab
        self.chave, self.x, self.y = chave, x, y

    def create(self):
        self.celula = self.sprite(self.chave.ladrilho_coisa, self.x, self.y)
        self.celula.scale.setTo(2.5, 2.5)
        self.celula.inputEnabled = True
        self.celula.frame = 160
        self.celula.events.onInputDown.add(lambda _=0, __=0: self.recebe(self.chave.aba_corrente.seleto), self)

    def recebe(self, item):
        if not item:
            return
        item.x, item.y = self.x+40, self.y+40


class Chaves(Actor):
    """Essa  é a classe Chaves que recebe os poderes da classe Circus de poder criar um jogo"""
    def __init__(self, x= BALONX, y= BALONY):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.aba_corrente = self.aba = None
        self.abas = "fruta objeto animal arma"
        self.ladrilho_coisa = "objeto"
        self.ladrilho_fruta = "fruta"
        self.ladrilho_animal = "animal"
        self.ladrilho_arvore = "arvore"
        self.ladrilho_fala = "chave"
        self.fala = self.falou =self.pensa = None
        self.fruta = self.animal = self.comida = None
        self.arvore = self.arma = self.objeto = None
        self.x, self.y = x, y
        self.jogo = None
        self.cria_tabuleiro()
        self.take_propils()
        self.ativo = True

    def ativa(self):
        """Abre o balão de conversa"""
        self.jogo.visible = self.ativo
        #self.tween(self.fala, 2000, repeat=0, alpha=1)
        self.ativo = not self.ativo


    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.spritesheet(self.ladrilho_fruta, IMG + "fruit.png", 65, 65, 8*8)
        self.spritesheet(self.ladrilho_animal, IMG + "largeemoji.png", 47.5, 47, 14*9)
        self.spritesheet(self.ladrilho_coisa, IMG + "cacarecos.png", 32, 32, 16*16)
        self.spritesheet(self.ladrilho_arvore, IMG + "treesprites1.png", 123.5, 111, 4*3)
        self.image(self.ladrilho_fala, IMG + "jogo_chaves.jpg")

    def take_propils(self):
        """Jogador escreve: hominídeo comer fruta_vermelha."""
        self.fruta = Take(self.ladrilho_fruta, 0, self.x+FALAX, self.y+FALAY)
        self.animal = Take(self.ladrilho_animal, 4*14+7, self.x+FALAX+FALASEPARA, self.y+FALAY)
        self.comida = Take(self.ladrilho_coisa, 5*16+6, self.x+FALAX+FALASEPARA*2, self.y+FALAY)
        #self.arvore = Take(self.ladrilho_arvore, 0, self.x+FALAX+FALASEPARA*2, self.y+FALAY)
        self.arma = Take(self.ladrilho_coisa, 16*4, self.x+FALAX+FALASEPARA*3, self.y+FALAY)
        self.objeto = Take(self.ladrilho_coisa, 16+7, self.x+FALAX+FALASEPARA*4, self.y+FALAY)
        self.aba_corrente = self.fruta

    def cria_tabuleiro(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        for x in range(4):
            for y in range(4):
                pass
                tab = None # self.sprite(self.ladrilho_coisa, TABUAX + x * TABUAS * 1.1, TABUAY + y * TABUAS)
                tab = Celula(self, tab, TABUAX+x*TABUAS*1.1, TABUAY+y*TABUAS)

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        self.fala = self.sprite(self.ladrilho_fala, self.x, self.y)
        self.jogo = self.group()
        self.fala.scale.setTo(2, 2)
        #self.fala.visible = False
        self.jogo.add(self.fala)

        def up(c=None, d=None):
            self.aba_corrente.rola(-1)

        def down(c=None, d=None):
            self.aba_corrente.rola(1)

        self.aba = self.group()
        self.aba.visible = False
        sobe = self.sprite(self.ladrilho_animal, self.x, self.y + 50 * 0)
        sobe.inputEnabled = True
        desce = self.sprite(self.ladrilho_animal, self.x, self.y + 50 * 4)
        sobe.frame = 14 * 9 - 4
        desce.inputEnabled = True
        desce.frame = 14 * 9 - 5
        sobe.events.onInputDown.add(up, self)
        desce.events.onInputDown.add(down, dict(b=1))
        self.jogo.add(sobe)
        self.jogo.add(desce)
        #self.jogo.visible = False


class Take(Actor):
    """Essa  é a classe Take que controla os personagens do jogo"""
    faz_sentido = [14*2+0, 14*2+1, 14*2+4, 14*2+5, 14*2+8,
                   14+0,  14+1, 14+2, 14+3, 14+4, 14+5, 14+6, 14+7, 14+8, 14+9,
                   70+0,70+1,70+2,70+3,70+4,70+5,70+6]
    def __init__(self, nome, frame, x, y):
        super().__init__()
        self.nome, self.frame, self.x, self.y = nome, frame, x, y
        self.aba = self.coisas = self.fala = self.jogo = None
        self.seleto = None

    def rola(self, desloca):
        """Aqui rolamos o conjunto de sprites mudando o frame de cada sprite"""
        self.frame += desloca
        for frame, coisa in enumerate(self.coisas):
            print(frame, coisa.frame)
            coisa.frame = self.frame + frame

    def create(self):
        """Aqui colocamos o sprite do homem e selecionamos o frame que o representa"""
        def up(c=None, d=None):
            self.frame += 1
            print("up",self.frame)
            for frame, coiso in enumerate(self.coisas):
                print(frame, coiso.frame)
                coiso.frame = self.frame + frame
        def down(c=None, d=None):
            self.frame -= 1
            print("down",self.frame)
            for frame, coiso in enumerate(self.coisas):
                coiso.frame = self.frame + frame
        self.aba = self.group()
        self.aba.visible = False
        self.coisas = [self._create(coisa) for coisa in range(1,4)]
        #self.jogo.visible = False

    def _create(self, frame):
        """Aqui colocamos o sprite do icon e selecionamos o frame que o representa"""
        coisa = self.sprite(self.nome, self.x, self.y+50*frame)
        coisa.frame = self.frame+frame
        #return coisa
        coisa.inputEnabled = True
        coisa.input.useHandCursor = True
        coisa.events.onInputDown.add(lambda a=None, b=frame, c=frame: self._click(b, c), dict(b=frame))
        coisa.anchor.setTo(0.5, 0.5)
        #self.jogo.add(coisa)
        #self.aba.add(coisa)
        return coisa

    def falou(self, fez_sentido=False):
        falou = self.frame + 1
        if fez_sentido:
            self.fala.frame = self.frame + 1
        else:
            self.fala.frame = 4*14+6
        return falou in self.faz_sentido


    def activate(self):
        self.aba.visible = True

    def _click(self, c=None, d=None):
        print("action", c, d)
        self.seleto = self._create(d-1)

    def update(self):
        pass

