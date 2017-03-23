from braser import Braser
from browser import doc


class Vitollino:
    _instance = None
    BRASER = None
    GID = "00000000000000000000"

    def __init__(self, w=800, h=800, mode=None, name="braser", states=None, alpha=False):
        self._init(w, h, mode, name, states, alpha)
        self.gamer = Vitollino.BRASER
        self.gamer.subscribe(self)
        self.game = self.gamer.game
        self.gid = "00000000000000000000"

    def set_id(self, gid):
        Vitollino.GID = gid
        print(gid)

    def _init(self, w=800, h=800, mode=None, name="braser", states=None, alpha=False):
        doc["pydiv"].html = ""
        Vitollino.BRASER = Braser(w, h, mode, name, states, alpha)
        Vitollino.BRASER.send('getid', {}, self.set_id, "GET")

    def preload(self):
        pass

    def create(self):
        pass

    def spritesheet(self, name, img, x=0, y=0, s=1):
        self.game.load.spritesheet(name, img, x, y, s)

    def group(self):
        return self.game.add.group()

    def tween(self, sprite, time, function="Linear", autostart=True, delay=0, repeat=-1, yoyo=False, **kwd):
        return self.game.add.tween(sprite).to(dict(kwd), time, function, autostart, delay, repeat, yoyo)

    def enable(self, item):
        self.game.physics.arcade.enable(item)

    def start_system(self):
        self.game.physics.startSystem(self.gamer.PHASER.Physics.ARCADE)

    def image(self, name, img):
        return self.game.load.image(name, img)

    def sprite(self, name, x=0, y=0):
        return self.game.add.sprite(x, y, name)

    def update(self):
        pass

    def score(self, evento, carta, ponto, valor):
        carta = '_'.join(carta)
        casa = '_'.join([str(evento.x), str(evento.y)])
        data = dict(doc_id=Vitollino.GID, carta=carta, casa=casa, move="ok", ponto=ponto, valor=valor)
        # self.gamer.send('store', data)
        print('store', data)

    def register(self, evento, carta, ponto, valor):
        carta = '_'.join(carta)
        data = dict(doc_id=Vitollino.GID, carta=carta, casa=evento, move="ok", ponto=ponto, valor=valor)
        # self.gamer.send('store', data)
        # print('register', data)



class Actor(Vitollino):
    def _init(self, w=800, h=800, mode=None, name="braser", states=None, alpha=False):
        pass
