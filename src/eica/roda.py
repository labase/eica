from braser.vitollino import Actor
from . import Ponto, Folha
from random import shuffle
from .eica import Jogo, Imagem, Botao
from .inventario import ListaInventario, Item

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
BALONX, BALONY = 20, 70
FALAX, FALAY, FALASEPARA = 100, 40, 100


class Roda(Jogo):
    """Essa  é a classe Roda que recebe os poderes da classe Circus de poder criar um jogo"""

    def __init__(self, x=BALONX, y=BALONY, acao=lambda _=0: None):
        super().__init__(ver=False)  # super é invocado aqui para preservar os poderes recebidos do Circus
        self.x, self.y, self.acao = x, y, acao
        # Imagem(Folha.cumulus, Ponto(x, y), self, (0.7, 0.7))
        # Imagem(Folha.cumulus, Ponto(x + FALAX + FALASEPARA * 3.7, 10), self, (0.5, 0.8))
        self.inventario = [
            ListaInventario(lambda _=0: None, Ponto(150+80*x, 90), item=[Folha.minitens], passo=Ponto(0, 50),
                            janela=3) for x in range(3)]
        Imagem(Folha.nuvem, Ponto(x, y-90), self, (2.0, 3.1))
        Imagem(Folha.cumulus, Ponto(x + FALAX + FALASEPARA * 3.7, -40), self, (1.6, 3.2))
        Botao(Folha.twosapiens, Ponto(250+x, 450+y-90), 0, self.activating, self, (0.22, 0.22))
        Botao(Folha.twosapiens, Ponto(250+x + FALAX + FALASEPARA * 2, 450+y-100), 2, self.activating, self, (0.22, 0.22))
        Botao(Folha.minitens, Ponto(x + FALAX + FALASEPARA * 2.5, y + FALAY + FALASEPARA), 39, self.activating, self)
        self.activating = self._click
        a, b, c = [(0, 540 + 80 * x, 30) for x in range(3)]
        self.texto = Fala(lambda _=0: None, Ponto(500, 90),
                          item=(Palavra(*a), Palavra(*b), Palavra(*c)), passo=Ponto(0, 50), janela=3)
        self.termos = None

    def ativa(self, ativo=None):
        """Abre o balão de conversa"""
        super().ativa(ativo)
        self.acao(not self.ativo)
        # self.tween(self.jogo, 1000, repeat=0, alpha=1)
        [inventario.ativa(self.ativo) for inventario in self.inventario]
        # [inventario.ativa(self.ativo) for inventario in self.texto.item]
        self.texto.ativa(self.ativo)
        self.score(evento=Ponto(x=0, y=0), carta="_ATIVA_", ponto="_LINGUA_", valor=self.ativo)

    def _nop(self, _=None, d=None):
        """Copia fala para pensamento do interlocutor"""
        pass

    def activating(self, _=None, d=None):
        """Copia fala para pensamento do interlocutor"""
        self.register(evento=self.activating, carta=["%s" % c for c in "abc"], ponto="_FALA_", valor=True)

    def _click(self, _=None, d=None):
        """Copia fala para pensamento do interlocutor"""
        fez_sentido = True  # set(termo.frame for termo in self.inventario) in faz_sentido
        carta = [termo.frame for termo in self.inventario]
        print("falou", carta, fez_sentido)
        self.score(evento=Ponto(x=0, y=0), carta=["%s" % c for c in carta], ponto="_FALA_", valor=fez_sentido)
        self.texto.fala(carta, fez_sentido)


class Fala(ListaInventario):
    """Essa  é a classe Take que controla os itens do jogo"""
    """Takes com retorno positivo"""
    faz_sentido = [14 * 2 + 0, 14 * 2 + 1, 14 * 2 + 4, 14 * 2 + 5, 14 * 2 + 8,
                   14 + 0, 14 + 1, 14 + 2, 14 + 3, 14 + 4, 14 + 5, 14 + 6, 14 + 7, 14 + 8, 14 + 9,
                   70 + 0, 70 + 1, 70 + 2, 70 + 3, 70 + 4, 70 + 5, 70 + 6]

    def __init__(self, recebe, ponto, delta=Ponto(300, 0), ver=False, item=None, passo=Ponto(0, 50), janela=6):
        super().__init__(recebe, ponto, delta, ver, item, passo, janela)

    def fala(self, carta, fez_sentido=False):
        frase = carta  # if fez_sentido else WTF
        [lista.append(palavra) for palavra, lista in zip(frase, self.item)]

    def monta_botoes(self):
        pass

    def ativa(self, ativo=None):
        """Abre o balão de conversa"""
        super().ativa(ativo)
        # self.tween(self.fala, 2000, repeat=0, alpha=1)
        for aba in self.abas:
            aba.mostra(False)
        for aba in self.item:
            aba.mostra(self.ativo)
        # self.aba_corrente.mostra(self.ativo)


class Palavra(Item):
    """Essa  é a classe Item que seve tanto como ítem como coleção de itens"""

    def __init__(self, frame=0, x=0, y=0, step=Ponto(0, 50), janela=6):
        super().__init__(lambda _=0: None, Folha.itens, frame, x, y, step, janela)
        self.range = list()
        self.n = self.nome = Folha.animal.n

    def append(self, palavra):
        self.range.append(palavra)
        self.coisas.append(self._create(palavra))
        self.rola(0)

    def mostra(self, muda):
        """ Mostra esta aba

        :param muda: booleano que diz se é para mostar ou ocultar a aba
        :return: None
        """
        self.aba.visible = muda
        self.range = list()
        for coisa in self.coisas:
            coisa.visible = False
        self.coisas = list()

    def _copy(self, frame):
        """Aqui colocamos o sprite do icon e selecionamos o frame que o representa"""
        displace = len(self.coisas)
        print("_copy", Folha.minitens, self.x + self.step.x * displace, self.y + self.step.y * displace, frame)
        coisa = self.sprite(Folha.minitens.n, self.x + self.step.x * displace, self.y + self.step.y * displace)
        coisa.frame = frame
        # coisa.scale.setTo(0.2, 0.2)
        self.aba.add(coisa)
        # self.aba.visible = True
        return coisa

    def rola(self, desloca):
        """Aqui rolamos o conjunto de sprites mudando o frame de cada sprite"""
        lista = len(self.range)
        self.range = (self.range + self.range + self.range)[lista + desloca: 2 * lista + desloca]
        for coisa in self.coisas:
            coisa.visible = False
        for frame, coisa in list(zip(self.range, self.coisas))[:self.janela]:
            # print(frame, coisa.frame)
            coisa.frame = frame
            coisa.visible = True
