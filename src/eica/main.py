from random import random
# from ..braser import Braser

DETAIL, DETAILURL = "dungeon_detail", "DungeonWall.jpg"
MONSTER, MONSTERURL = "monster", "monstersheets.png?"
DETILE = "dungeon_detile"


class Masmorra:
    def __init__(self, gamer):
        self.gamer = gamer(800, 600, gamer.AUTO, 'flying-circus')
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
        rotate = 0
        for i in range(6):
            for j in range(5):
                detail = self.game.add.sprite(64+i * 128, 64+j * 128, DETILE)
                detail.anchor.setTo(0.5, 0.5)
                detail.angle = rotate
                detail.frame = (6*j+i) % 12
                rotate += 90

        sprite = self.game.add.sprite(20, 148, MONSTER)
        # sprite.animations.add('ani', [0, 1, 2, 3, 16+0, 16+1, 16+2, 16+3], 2, True)
        sprite.animations.add('ani', [0, 1, 2, 3], 4, True)
        sprite.play('ani')

        sprite = self.game.add.sprite(148, 148, MONSTER)
        # sprite.animations.add('mon', [7*16+0, 7*16+1, 7*16+2, 7*16+3, 7*16+16 + 0,
        #                               7*16+16 + 1, 7*16+16 + 2, 7*16+16 + 3], 4, True)
        sprite.animations.add('mon', [6*16+0, 6*16+1, 6*16+2, 6*16+3], 4, True)
        sprite.play('mon')

    def update(self):
        pass


class Main:
    def __init__(self, Game, Phaser):
        self.ph = Phaser
        self.game = Game(800, 600, Phaser.AUTO, 'flying-circus',
                         {"preload": self.preload, "create": self.create, "update": self.update})
        self.player = self.platforms = self.cursors = self.stars = self.scoreText = None
        self.score = 0
        pass

    def preload(self, *_):
        self.game.load.image('image-url', 'assets/sky.png')

        self.game.load.image('ground', 'assets/platform.png')
        self.game.load.image('star', 'assets/star.png')
        self.game.load.spritesheet('dude', 'assets/dude.png', 32, 48)

    def create(self, *_):
        self.game.physics.startSystem(self.ph.Physics.ARCADE)
        self.game.add.sprite(0, 0, 'image-url')
        self.game.add.sprite(0, 0, 'star')
        platforms = self.game.add.group()
        platforms.enableBody = True
        ground = platforms.create(0, self.game.world.height - 64, 'ground')
        ground.scale.setTo(2, 2)
        ground.body.immovable = True
        ledge = platforms.create(400, 400, 'ground')

        ledge.body.immovable = True

        ledge = platforms.create(-150, 250, 'ground')

        ledge.body.immovable = True

        player = self.game.add.sprite(32, self.game.world.height - 150, 'dude')

        #  We need to enable physics on the player
        self.game.physics.arcade.enable(player)

        #  Player physics properties. Give the little guy a slight bounce.
        player.body.bounce.y = 0.2
        player.body.gravity.y = 300
        player.body.collideWorldBounds = True

        #  Our two animations, walking left and right.
        player.animations.add('left', [0, 1, 2, 3], 10, True)
        player.animations.add('right', [5, 6, 7, 8], 10, True)

        self.cursors = self.game.input.keyboard.createCursorKeys()
        stars = self.game.add.group()

        stars.enableBody = True
        # return

        #  Here we'll create 12 of them evenly spaced apart
        for i in range(12):

            #  Create a star inside of the 'stars' group
            star = stars.create(i * 70, 0, 'star')

            #  Let gravity do its thing
            star.body.gravity.y = 6

            #  This just gives each star a slightly random bounce value
            star.body.bounce.y = 0.7 + random() * 0.2
        self.scoreText = self.game.add.text(16, 16, 'score: 0', dict(fontSize='32px', fill='#000'))
        self.player, self.platforms, self.stars = player, platforms, stars

    def update(self, *arg):
        cursors, player, platforms, stars = self.cursors, self.player, self.platforms, self.stars

        #  Collide the player and the stars with the platforms
        self.game.physics.arcade.collide(self.player, self.platforms)

        player.body.velocity.x = 0

        if cursors.left.isDown:
            #  Move to the left
            player.body.velocity.x = -150

            player.animations.play('left')
        elif cursors.right.isDown:
            #  Move to the right
            player.body.velocity.x = 150

            player.animations.play('right')
        else:
            #  Stand still
            player.animations.stop()

            player.frame = 4

        #  Allow the player to jump if they are touching the ground.
        if cursors.up.isDown and player.body.touching.down:
            player.body.velocity.y = -350

        def collectstar(_, star):
            # Removes the star from the screen
            star.kill()
            self.score += 10
            self.scoreText.text = 'Score: %d' % self.score

        self.game.physics.arcade.collide(stars, platforms)

        self.game.physics.arcade.overlap(player, stars, collectstar, None, self)


def main(Game):
    Masmorra(Game)
    # Main(Game, auto)
