from braser import Braser
from browser import doc


class Vitollino:
    _instance = None
    BRASER = None

    def __init__(self):
        self._init()
        self.gamer = Vitollino.BRASER
        self.gamer.subscribe(self)
        self.game = self.gamer.game

    def _init(self):
        doc["pydiv"].html = ""
        Vitollino.BRASER = Braser(800, 800)

    def preload(self):
        pass

    def create(self):
        pass

    def spritesheet(self, name, img, x=0, y=0, s=1):
        self.game.load.spritesheet(name, img, x, y, s)

    def group(self):
        return self.game.add.group()

    def tween(self, sprite, time, function="Linear", autostart=True, delay=0, repeat=-1, yoyo=False, **kwd):
        return self.game.add.tween(sprite).to(dict(kwd), time, function, autostart, delay, repeat, yoyo);

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


class Actor(Vitollino):
    def _init(self):
        pass
