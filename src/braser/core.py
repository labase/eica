from braser import JsPhaser


class Braser:
    """
    Brython object-oriented  wrapper for js Phaser.

    :param x: Canvas width.
    :param y: Canvas height.
    :param mode: Canvas mode.
    :param name: Game name.
    :param keyargs: Extra arguments
    """
    PHASER = JsPhaser().phaser()
    AUTO = JsPhaser().phaser().AUTO
    Game = JsPhaser().BraserGame

    def __init__(self, x=800, y=600, mode=None, name="braser", **kwargs):
        mode = mode or Braser.AUTO
        print(Braser.AUTO, Braser.PHASER)
        self.game = Braser.Game(x, y, mode, name,
                                {"preload": self.preload, "create": self.create, "update": self.update})
        self.subscribers = []

    def subscribe(self, subscriber):
        """
        Subscribe elements for game loop.

        :param subscriber:
        """
        self.subscribers.append(subscriber)

    def preload(self, *_):
        """
        Preload element.

        """
        for subscriber in self.subscribers:
            subscriber.preload()

    def create(self, *_):
        """
        Create element.

        """
        for subscriber in self.subscribers:
            subscriber.create()

    def update(self, *_):
        """
        Update element.

        """
        for subscriber in self.subscribers:
            subscriber.update()
