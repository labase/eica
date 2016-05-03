from browser import window
from javascript import JSConstructor


class JsPhaser(object):
    """
    Brython wrapper for Phaser.

    :return: Instance of JsPhaser.
    """
    _instance = None
    PHASER = window.Phaser
    JSC = JSConstructor
    BraserGame = JSConstructor(PHASER.Game)

    def __new__(cls):

        if not cls._instance:
            cls._instance = super(JsPhaser, cls).__new__(cls)
        print("JsPhaser__new__")
        return cls._instance

    def phaser(self):
        """
        Javascript Phaser.

        :return: A Python reference for js Phaser.
        """
        return JsPhaser.PHASER

    def construct(self, constructor):
        """
        Construct a Python version of a js Constructor.

        :param constructor: Js Constructor to be called.
        :return: The Python wrapper for the given js Constructor.
        """
        return JsPhaser.JSC(constructor)

__all__ = ["core"]
from braser.core import Braser



