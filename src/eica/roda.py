from braser.vitollino import Actor
from . import Ponto
from random import random

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
BALONX, BALONY = 20, 70
FALAX, FALAY, FALASEPARA = 100, 40, 100

class Roda(Actor):
    """Essa  é a classe Roda que recebe os poderes da classe Circus de poder criar um jogo"""
    def __init__(self, x= BALONX, y= BALONY):
        super().__init__()  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.ladrilho_coisa = "roda"
        self.ladrilho_fala = "fala"
        self.fala = self.falou =self.pensa = None
        self.nome = self.verbo = self.alvo = None
        self.x, self.y = x, y
        self.jogo = None
        self.take_propils()
        self.ativo = True

    def ativa(self):
        """Abre o balão de conversa"""
        self.jogo.visible = self.ativo
        self.tween(self.jogo, 1000, repeat=0, alpha=1)
        self.score(evento=Ponto(x=0, y=0), carta="0", ponto="_LINGUA_", valor=self.ativo)
        self.ativo = not self.ativo


    def preload(self):
        """Aqui no preload carregamos a imagem mundo e a folha de ladrilhos dos homens"""
        self.spritesheet(self.ladrilho_coisa, IMG + "largeemoji.png", 47.5, 47, 14*9)
        self.image(self.ladrilho_fala, IMG + "balooni.png")

    def take_propils(self):
        """Jogador escreve: hominídeo comer fruta_vermelha."""
        self.nome = Take(self.ladrilho_coisa, 14*2, self.x+FALAX, self.y+FALAY)
        self.verbo = Take(self.ladrilho_coisa, 14, self.x+FALAX+FALASEPARA, self.y+FALAY)
        self.alvo = Take(self.ladrilho_coisa, 14*5, self.x+FALAX+FALASEPARA*2, self.y+FALAY)

    def create(self):
        """Aqui colocamos os sprites da fala"""
        """Balao de fala"""
        self.fala = self.sprite(self.ladrilho_fala, self.x, self.y)
        self.fala.scale.setTo(0.7, 0.7)

        self.jogo = self.group()
        self.nome.jogo = self.verbo.jogo = self.alvo.jogo = self.jogo

        """Balao de pensamento"""
        self.pensa = self.sprite(self.ladrilho_fala, self.x+FALAX+FALASEPARA*3.7, self.y)
        self.pensa.scale.setTo(0.5, 0.5)

        """Botao de falar"""
        self.falou = self.sprite(self.ladrilho_coisa, self.x+FALAX+FALASEPARA*2.5, self.y+FALAY+FALASEPARA)
        self.falou.frame = 14*3
        self.falou.inputEnabled = True
        self.falou.scale.setTo(0.7, 0.7)
        self.falou.events.onInputDown.add(self._click, self)

        self.jogo.add(self.fala)
        self.jogo.add(self.pensa)
        self.jogo.add(self.falou)
        self.jogo.alpha = 0
        #self.jogo.visible = False

    def _click(self, c=None, d=None):
        """Copia fala para pensamento do interlocutor"""
        faz_sentido = self.nome.falou() and self.verbo.falou() and self.alvo.falou()
        carta = [self.nome.frame, self.verbo.frame, self.alvo.frame]
        print("falou", carta, faz_sentido)
        self.score(evento=Ponto(x=0, y=0), carta=["%s" % c for c in carta], ponto="_FALA_", valor=faz_sentido)

        self.nome.falou(faz_sentido)
        self.verbo.falou(faz_sentido)
        self.alvo.falou(faz_sentido)


class Take(Actor):
    """Essa  é a classe Take que controla os itens do jogo"""
    """Takes com retorno positivo"""
    faz_sentido = [14*2+0, 14*2+1, 14*2+4, 14*2+5, 14*2+8,
                   14+0,  14+1, 14+2, 14+3, 14+4, 14+5, 14+6, 14+7, 14+8, 14+9,
                   70+0,70+1,70+2,70+3,70+4,70+5,70+6]

    def __init__(self, nome, frame, x, y):
        super().__init__()
        self.nome, self.frame, self.x, self.y = nome, frame, x, y
        self.coisa = self.coisas = self.fala = self.jogo = None

    def create(self):
        """Aqui criamos as funçoes para subir ou descer a roda"""
        def up(c=None, d=None):
            self.frame += 1
            print("up",self.frame)
            for frame, coisa in enumerate(self.coisas):
                print(frame, coisa.frame)
                coisa.frame = self.frame + frame
        def down(c=None, d=None):
            self.frame -= 1
            print("down",self.frame)
            for frame, coisa in enumerate(self.coisas):
                coisa.frame = self.frame + frame

        self.coisas = [self._create(coisa) for coisa in range(1,4)]
        self.fala = self.sprite(self.nome, self.x+FALAX//2+FALASEPARA*3.5, self.y+FALAY)
        self.jogo.add(self.fala)
        self.fala.frame = self.frame + 2

        """Coloca os sprites dos botoes de subir e descer"""
        sobe = self.sprite(self.nome, self.x-25, self.y + 50 * 0)
        sobe.inputEnabled = True
        desce = self.sprite(self.nome, self.x-25, self.y + 50 * 3.5)
        sobe.frame = 14 * 9 - 4
        desce.inputEnabled = True
        desce.frame = 14 * 9 - 5
        sobe.events.onInputDown.add(up, self)
        desce.events.onInputDown.add(down, dict(b=1))

        self.jogo.add(sobe)
        self.jogo.add(desce)
        self.jogo.visible = False

    def _create(self, frame):
        """Aqui colocamos o sprite do icon e selecionamos o frame que o representa"""
        coisa = self.sprite(self.nome, self.x, self.y+50*frame)
        coisa.inputEnabled = True
        coisa.input.useHandCursor = True
        coisa.frame = self.frame+frame
        coisa.events.onInputDown.add(lambda a=None, b=frame, c=frame: self._click(b, c), dict(b=frame))
        coisa.anchor.setTo(0.5, 0.5)
        self.jogo.add(coisa)
        return coisa

    def falou(self, fez_sentido=False):
        falou = self.frame + 1
        if fez_sentido:
            self.fala.frame = self.frame + 1
        else:
            self.fala.frame = 4*14+6
        return falou in self.faz_sentido


    def activate(self, action=lambda: None):
        self.act = action

    def _click(self, c=None, d=None):
        print("action", c, d)

    def update(self):
        pass

