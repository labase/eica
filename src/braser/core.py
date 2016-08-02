from braser import JsPhaser
from browser.ajax import ajax


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
    CANVAS = JsPhaser().phaser().CANVAS
    Game = JsPhaser().BraserGame

    def __init__(self, x=800, y=600, mode=None, name="braser", **kwargs):
        mode = mode or Braser.CANVAS
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

    def send(self, operation, data, action=lambda t: None, method="POST"):
        def on_complete(request):
            if int(request.status) == 200 or request.status == 0:
                # print("req = ajax()== 200", request.text)
                action(request.text)
            else:
                print("error " + request.text)

        req = ajax()
        req.bind('complete', on_complete)
        # req.on_complete = on_complete
        url = "/record/" + operation
        req.open(method, url, True)
        # req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.set_header("Content-Type", "application/json; charset=utf-8")
        # print("def send", data)
        req.send(data)
