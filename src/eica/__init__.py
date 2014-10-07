#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
EICA World Game - INIT
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/09/17
:Status: This is a "work in progress"
:Revision: 0.2.2
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

.. _mod_eica

"""
__version__ = "0.2.2"

IMG = "https://dl.dropboxusercontent.com/u/1751704/igames/img/"
SPRITE_DIMENSIONS = dict(
    mundo=["eicamundo", 512, 1, 1], fog=["Fog04", 512, 1, 1], foghole=["Foghole", 512, 1, 1],
    tree=["treesprite", 120, 4, 8], fruit=["fruit", 65, 6, 12], caver=["caveman", 125, 5, 10],
    debris=["cacarecos", 32, 12, 48], emoji=["largeemoji", 47, 14, 4*14], baloon=["baloons", 600, 2, 2])
SPRITE_DIMENSIONS = [[key] + [value[0] + '.png']
                     + [it for it in value[1:]] for key, value in SPRITE_DIMENSIONS.items()]


def main():
    from browser import document, html
    from __random import randint, shuffle
    from crafty import Crafty

    class World:
        def __init__(self):
            def cut_sprites(name, image, sprite_size, columns, total_pictures):
                spritenames = {
                    "%s%d" % (name, index): [index % columns, index//columns]
                    for index in range(total_pictures)}
                print(spritenames, image, sprite_size)
                crafty.sprites(sprite_size, IMG+image, **spritenames)
            self.talking = True
            self.talk = self._talk
            self.doc = document['game']
            print(SPRITE_DIMENSIONS)
            self.crafty = crafty = Crafty(512, 512, self.doc)
            [cut_sprites(*args) for args in SPRITE_DIMENSIONS]
            m = crafty.e('2D, Canvas, Tween, mundo0').attr(alpha=1.0, x=0, y=0, w=512, h=512, _globalZ=10)
            ''''''
            self.foh = foh = crafty.e('2D, Canvas, Tween, foghole0').attr(x=0, y=0, w=512, h=512, _globalZ=20)
            self.fog = fog = crafty.e('2D, Canvas, Mouse, Tween, Text, fog0')\
                .attr(alpha=0.95, x=0, y=0, w=512, h=512, _globalZ=30)
            self.ver = crafty.e('2D, Canvas, Tween, Text')\
                .attr(alpha=1.0, x=400, y=2, w=100, h=50, _globalZ=50).text("Version %s" % __version__)
            fog.onebind("Click", self.clicked)
            fog.onebind("TweenEnd", self.showtrees)
            ''''''
            self.ugh = ugh = Caveman(i=4, x=100, y=200, crafty=crafty, world=self)
            self.agh = agh = Caveman(i=6, x=240, y=265, crafty=crafty, world=self)
            """
            self.fruitfall()
            """
            #self.fogfade()

        def _notalk(self, ev=None):
            print('wo notalk')
            self.talking = not self.talking
            self.ugh.notalk(self.talking)
            self.agh.notalk(self.talking)

        def _talk(self, ev=None):
            print('wo talk')
            self.talk = self._notalk
            self.ugh.talk(None)
            self.agh.talk(None)

        def clicked(self, ev=None):
            print('clickeed')
            self.fog.tween(3000, alpha=0.0)

        def fogfade(self):
            print('fogfade')
            self.foh.tween(3000, alpha=0.0)
            debris = list(range(48))
            shuffle(debris)
            for drs, fig in enumerate(debris[:20]):
                Debris(drs, fig, self.crafty, self)

        def fruitfall(self):
            print('fruitfall')
            for fruit in range(12):
                self.crafty.e('2D, Canvas, Tween, fruit%d' % fruit)\
                    .attr(x=280 + 20*fruit//3, y=140+20*fruit % 3, w=16, h=16, _globalZ=14)\
                    .tween(randint(100, 3000), y=140+10+20*fruit % 3)

        def showtrees(self, ev=None):
            print('showtrees')
            for i in range(8):
                Tree(i, self.crafty, self)

        def matchdebris(self, debris):
            print('matchdebris')
            if Debris.TI < 12:
                debris.position(None)

    class Caveman:

        def __init__(self, i, x, y, crafty, world):
            print('Caveman __init__', i)
            self.world = world
            self.i = i
            self._b = None
            self.xy = (x, y)
            self.crafty = crafty
            self._t = crafty.e('2D, Canvas, Mouse, Tween, caver%d' % i)\
                .attr(x=x, y=y, w=25, h=25, _globalZ=17)
            self._t.bind("Click", self.click)
            self._talking = []

        def click(self, i):
            print('Caveman clickeed')
            self.world.talk(i)

        def notalk(self, talking=False):
            print('Caveman no_talk')
            self._b.visible = talking
            for lang in self._talking:
                lang.visible = talking

        def talk(self, i):
            print('Caveman clickeed')
            x, y = self.xy
            WR_OFF, WR_SZ = (self.i//5*130), (self.i//5*30)
            self._b = self.crafty.e('2D, Canvas, Tween, baloon%d' % (self.i//5))\
                .attr(x=x-100+WR_OFF, y=y-200, w=200+WR_SZ, h=200, _globalZ=18)
            self._talking = [
                self.crafty.e('2D, Canvas, Tween, emoji%d' % em)
                    .attr(x=x-75+WR_OFF + 55*em//3, y=y-180+40*em % 3+WR_SZ//2, w=38, h=38, _globalZ=19)
                for em in range(9)
            ]

        def move(self, x, y, action):
            print('Cavemanmove', x, y)
            self._t.tween(1000, x=x, y=y)
            self._t.onebind('TweenEnd', action)

    class Tree:
        TI = 0

        def __init__(self, i, crafty, world):
            print('Treeclickeed__init__', i)
            self.world = world
            self.i = i
            self._t = crafty.e('2D, Canvas, Mouse, Tween, tree%d' % i)\
                .attr(x=10 + 300*i//4, y=10+120*i % 4, w=100, h=100, _globalZ=100)
            self._t.bind("Click", self.click)
            self._click = self._position

        def click(self, i):
            self._click(i)

        def _position(self, i):
            print('Treeclickeed', Tree.TI)

            ti = Tree.TI
            dx, dy = randint(0, 14), randint(0, 14)
            self._t.tween(200, x=140+dx+25*ti//3, y=180+dx+25*ti % 3, w=20, h=20)
            Tree.TI += 1
            self._click = self._brake
            if Tree.TI >= 8:
                self.world.fogfade()

        def _brake(self, i):
            print('_brake', self.i)
            if self.i == 5:
                self.world.fruitfall()
                self._click = lambda ev=0: None

    class Debris:
        TI = 0

        def __init__(self, drs, fig, crafty, world):
            print('Treeclickeed__init__', i)
            self.world = world
            self.i = i
            dx, dy = randint(0, 20), randint(0, 10)
            self._t = crafty.e('2D, Canvas, Mouse, Tween, debris%d' % fig)\
                .attr(x=360+dx+16*drs//4, y=134+dy+16*drs % 4, w=16, h=16, _globalZ=15)

            self._t.bind("Click", self.click)

        def click(self, i):
            self.world.matchdebris(self)

        def position(self, i):
            print('Debris clickeed', Debris.TI)

            ti = Debris.TI
            dx, dy = randint(0, 5), randint(0, 5)
            self._t.tween(200, x=280+dx+16*ti//3, y=154+dx+16*ti % 3, w=16, h=16)
            Debris.TI += 1

    World()
