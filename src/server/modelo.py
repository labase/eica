__author__ = 'carlo'
from tinydb import TinyDB, where
import os
# from tinydb.storages import MemoryStorage
from uuid import uuid1
# DBM = lambda :TinyDB(storage=MemoryStorage)

JSONDB = os.path.dirname(__file__) + '/eica.json'

DBF = lambda: TinyDB(JSONDB)


class Pessoa:
    def __init__(self, base=DBF):
        self.banco = base()

    def __setitem__(self, key, value):
        if self.banco.contains(where('key') == key):
            self.banco.update(dict(value=value), where('key') == key)
        else:
            self.banco.insert(dict(key=key, value=value))

    def __getitem__(self, key):
        return self.banco.search(where('key') == key)[0]['value']

    def save(self, value):
        key = str(uuid1())
        self.banco.insert(dict(key=key, value=value))
        return key


class Banco:
    def __init__(self, base=DBF):
        self.banco = base()

    def __setitem__(self, key, value):
        if self.banco.contains(where('key') == key):
            self.banco.update(dict(value=value), where('key') == key)
        else:
            self.banco.insert(dict(key=key, value=value))

    def __getitem__(self, key):
        return self.banco.search(where('key') == key)[0]['value']

    def save(self, value):
        key = str(uuid1())
        self.banco.insert(dict(key=key, value=value))
        return key

    def get(self, key):
        return self[key]

    def set(self, key, value):
        self[key] = value


def tests():
    from tinydb.storages import MemoryStorage

    b = Banco(lambda: TinyDB(storage=MemoryStorage))
    b[1] = 2
    assert b[1] == 2, "falhou em recuperar b[1]: %s" % str(b[1])
    b[1] = 3
    assert b[1] == 3, "falhou em recuperar b[1]: %s" % str(b[1])
    c = b.save(4)
    assert b[c] == 4, "falhou em recuperar b[1]: %s" % str(b[c])


if __name__ == "__main__":
    tests()
else:
    DRECORD = Banco()
