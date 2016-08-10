# -*- coding: UTF8 -*-
from tinydb import TinyDB, Query
import os
# from tinydb.storages import MemoryStorage
from uuid import uuid1
# DBM = lambda :TinyDB(storage=MemoryStorage)

JSONDB = os.path.dirname(__file__) + '/eica.json'

DBF = lambda: TinyDB(JSONDB)
__author__ = 'carlo'

'''
db = TinyDB(JSONDB)

todos = db.all()
User = Query()

validos = db.search(User.value.exists())

print(validos[0])

vale = set(registro["value"]["user"] for registro in validos)

for num, registro in enumerate(vale):
    print(num, registro)
'''


class Banco:
    def __init__(self, base=DBF):
        self.banco = base()
        self.query = Query()
        self.users = []

    def __setitem__(self, key, value):
        if self.banco.contains(where('key') == key):
            self.banco.update(dict(value=value), where('key') == key)
        else:
            self.banco.insert(dict(key=key, value=value))

    def __getitem__(self, key):
        return self.banco.search(where('key') == key)[0]['value']

    def find_all_users(self):
        self.users = self.banco.search(self.query.value.exists())
        return self.users

    def use_with_caution_removes_records_fro_db(self, id_list_to_be_removed):
        self.banco.remove(eids=id_list_to_be_removed)

    def list_users_and_moves(self):
        banco = self
        nousers = "carlo carla Jonatas ggggg".split()
        for usr in banco.find_all_users():
            print(usr["value"]["user"], len(usr["value"]["jogada"]))
        print("##############################")

    def use_with_caution_clean_db(self, id_list_to_be_removed=None):
        banco = self
        nousers = id_list_to_be_removed or "carlo carla Jonatas ggggg".split()
        for usr in banco.find_those_users(nousers):
            print(usr)
        print("##############################")
        nousers_ids = banco.find_those_users_ids(nousers)
        print(nousers_ids)
        banco.use_with_caution_removes_records_fro_db(banco.find_those_users_ids(nousers))
        for usr in banco.find_those_users(nousers):
            print(usr)

    def find_those_users(self, names):
        users = self.banco.search(self.query.value.user.exists())
        return [(a.eid, a["value"]["user"]) for a in users if a["value"]["user"] in names]

    def find_all_users_names(self):
        users = self.banco.search(self.query.value.user.exists())
        return [a["value"]["user"] for a in users]

    def find_those_users_ids(self, names):
        users = self.banco.search(self.query.value.user.exists())
        return [a.eid for a in users if a["value"]["user"] in names]

    def find_inconsistent_users_ids(self, name):
        users = self.banco.search(self.query.value.user == name)
        dem = ["user", "idade", "sexo", "ano"]
        valueset = set(next((dado for dado in list(val["value"].items()) if dado[0] in dem) for val in list(users)))
        dados = {dado[0]: dado[1] if dado[0] != "idade" else int(dado[1].replace("anos", "")) + 5 for dado in valueset}
        return dados

    def save(self, value):
        key = str(uuid1())
        self.banco.insert(dict(key=key, value=value))
        return key

if __name__ == '__main__':
    banco = Banco()
    unique = set(banco.find_all_users_names())
    values = [banco.find_inconsistent_users_ids(name) for name in unique]
    for i, name in enumerate(values):
        print(i, "nome:{user: >40}  idade: {idade: >4}   ano: {ano}     genero: {sexo}".format(**name))
