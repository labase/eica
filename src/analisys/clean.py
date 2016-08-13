# -*- coding: UTF8 -*-
from tinydb import TinyDB, Query
import os
# from tinydb.storages import MemoryStorage
from uuid import uuid1
from datetime import datetime as dt
from time import strftime
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

    def merge_sessions_ordered(self, given_user):
        user_sessions = self.banco.search(self.query.value.user == given_user)
        value_keys = ("tempo", "carta", "casa", "valor", "ponto")
        tuple_session_values_content = [tuple([jogada[termo] for termo in value_keys])
                                        for sessions in user_sessions for jogada in sessions["value"]["jogada"]]
        sorted(tuple_session_values_content)
        dict_session_values = [{key: value for key, value in zip(value_keys, values)}
                               for values in tuple_session_values_content]
        return dict_session_values

    def caution_update_user_with_merged_data(self, given_user):
        given_user_merged_dict_list = self.merge_sessions_ordered(given_user)
        user_sessions = self.banco.search(self.query.value.user == given_user)
        user_sessions[0]["value"]["jogada"] = given_user_merged_dict_list
        given_user_other_ids_to_be_removed = [session.eid for session in user_sessions[1:]]
        self.banco.remove(eids=given_user_other_ids_to_be_removed)
        return given_user_other_ids_to_be_removed

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
        jogada = [item for sublist in users for item in sublist["value"]['jogada']]
        dados = {dado[0]: dado[1] if dado[0] != "idade" else int(dado[1].replace("anos", "")) + 5 for dado in valueset}
        # jogada = users[0]["value"]['jogada']

        dados.update(dict(hora=jogada[0]["tempo"] if jogada else 0))
        return dados

    def report_no_user_data(self):
        banco = self
        unique = set(banco.find_all_users_names())
        values = [banco.find_inconsistent_users_ids(name) for name in unique]
        values = [value for value in values if value["hora"] == 0]
        report = "nome:{user: >40}  idade: {idade: >4}   ano: {ano}   dia+hora: {hora} genero: {sexo} "
        for i, name in enumerate(values):
                print("{:3d}".format(i), report.format(**name))

    def report_user_data(self):
        banco = self
        unique = set(banco.find_all_users_names())
        values = [banco.find_inconsistent_users_ids(name) for name in unique]
        values = [value for value in values if value["hora"] != 0]
        dem = ["user", "idade", "sexo", "ano", "hora"]
        valuetuple = [tuple(line[key] for key in dem) for line in values]
        valuetuple.sort(key=lambda tp: tp[0].lower().replace(" ", ""))
        values = [{key: value for key, value in zip(dem, line)} for line in valuetuple]
        report = "nome:{user: >40}  idade: {idade: >4}   ano: {ano}   dia+hora: {hora} genero: {sexo} "
        for i, name in enumerate(values):
            jogadas = sum(len(copy["value"]["jogada"])
                          for copy in self.banco.search(self.query.value.user == name["user"]))
            tempos = [copy["value"]["jogada"]
                      for copy in self.banco.search(self.query.value.user == name["user"])]
            tempos = [lance["tempo"] for copy in tempos for lance in copy]
            # tempo = strptime(max(tempos), "%c")-strptime(min(tempos), "%c")
            timeformat = "%Y-%m-%d %H:%M:%S"
            tempo = dt.strptime(max(tempos).split(".")[0], timeformat)-dt.strptime(min(tempos).split(".")[0], timeformat)
            print("{:3d}".format(i), "Lances: {:3d}".format(jogadas), "T:{:>9}".format(str(tempo)), report.format(**name))

    def rename_user_with_inconsistent_names(self):
        users = [("ana fernanda dos santos", "ana fernanda dos santos "),
                 ("christian rodrigues gago", "christian"),
                 ("evellyn vitoria feitosa araujo", "evellyn"),
                 ("Ester Helen Rodrigues Cordeiro de Brito", "ESTERHELENRODRIGUESCORDEIRODEBRITO"),
                 ("jade feitosa matias dos santos", "jade", "jady  feitosa ", "jady  feitosa"),
                 ("julia gabrielly nascimento marques", "julia gabrielly nacismento marqeus", "julia"),
                 ("kamille de oliveira", "kamille de olivera "),
                 ("laiza fernandes de farias", "laiza"),
                 ("samuel gomes", "samuel"),
                 ("tatiane monteiro nascimento", "tiane monteiro nascimento"),
                 ]
        # users = [tuple(" ".join(nome.capitalize() for nome in item.split()) if i == 0) for i, item in enumerate(user)]
        masters = [" ".join(nome.capitalize() for nome in tup[0].split(" ")) for tup in users]
        print(masters)
        for master, user in zip(masters, users):
            allcopies = [(master, record.eid, record["value"]["user"], record["value"])
                         for u_name in user
                         for record in self.banco.search(self.query.value.user == u_name)]
            # print(allcopies)
            for _, oid, name, values in allcopies:
                values["user"] = master
                self.banco.update(dict(value=values), eids=[oid])

    def report_merged_user(self, user="tatiane monteiro nascimento"):
        banco = self
        merge_sorted_data = self.merge_sessions_ordered(user)
        for i, data in enumerate(merge_sorted_data):
            print(i, data)
            # print(i, "nome:{user: >40}  idade: {idade: >4}   ano: {ano}     genero: {sexo}".format(**name))

    def save(self, value):
        key = str(uuid1())
        self.banco.insert(dict(key=key, value=value))
        return key


if __name__ == '__main__':
    banco = Banco()
    banco.report_user_data()
    # banco.report_no_user_data()
    # banco.rename_user_with_inconsistent_names()

