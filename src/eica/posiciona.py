# from ..braser import Braser

DETAIL, DETAILURL = "dungeon_detail", "DungeonWall.jpg"
MONSTER, MONSTERURL = "monster", "monstersheets.png?"
DETILE = "dungeon_detile"


class Masmorra:
    def __init__(self, gamer):
        self.gamer = gamer(800, 600, gamer.AUTO, 'eica')
        self.gamer.subscribe(self)
        self.game = self.gamer.game
        self.ph = self.gamer.PHASER

    def preload(self):
        # self.game.load.image(DETAIL, DETAILURL)
        self.game.load.spritesheet(MONSTER, MONSTERURL, 64, 63, 16*12)
        self.game.load.spritesheet(DETILE, DETAILURL, 128, 128, 12)

    def create(self):
        self.game.physics.startSystem(self.ph.Physics.ARCADE)
        detail = self.game.add.sprite(0, 0, DETILE)
        #detail.anchor.setTo = (0.5, 0.5)
        #detail.anchor.x, detail.anchor.y = (0.5, 0.5)
        detail.frame = 0
        #detail.angle = 270

        detail2 = self.game.add.sprite(128, 0, DETILE)
        detail2.frame = 1

        detail3 = self.game.add.sprite(0+64, 128+64, DETILE)
        detail3.anchor.x, detail3.anchor.y = (0.5, 0.5)
        detail3.frame = 0
        detail3.angle = 270

        detail4 = self.game.add.sprite(128+64, 128+64, DETILE)
        detail4.frame = 1
        detail4.anchor.x, detail4.anchor.y = (0.5, 0.5)
        detail4.angle = 90

    def update(self):
        pass


def main(game):
    Masmorra(game)
