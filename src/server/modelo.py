__author__ = 'carlo'
import os
from redislite import Redis
# from tinydb.storages import MemoryStorage
from uuid import uuid1
# DBM = lambda :TinyDB(storage=MemoryStorage)

JSONDB = os.path.dirname(__file__) + '/eica.json'

DBF = lambda: Redis(JSONDB)


class Banco:
    def __init__(self, base=DBF):
        self.banco = base()

    def save(self, value):
        key = str(uuid1())
        self.banco.set(key, value)
        return key

    def get(self, key):
        return self.banco.get(key)

    def set(self, key, value):
        self.banco.set(key, value)
        return key


def tests():

    b = Banco(lambda: Redis('/tmp/redis.db'))
    b.set(1, 2)
    assert b.get(1) == 2, "falhou em recuperar b[1]: %s" % str(b.get(1))
    print("assert b.get(1) == 2", str(b.get(1)))
    b.set(1, 3)
    assert b.get(1) == 3, "falhou em recuperar b[1]: %s" % str(b.get(1))
    c = b.save(4)
    assert b.get(c) == 4, "falhou em recuperar b[1]: %s" % str(b.get(c))


if __name__ == "__main__":
    print("TESTS", Banco())
    tests()
else:
    print("DRECORD", Banco())
    DRECORD = Banco()
