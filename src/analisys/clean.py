# -*- coding: UTF8 -*-
from tinydb import TinyDB, Query
from tinydb.operations import delete
import os
# from tinydb.storages import MemoryStorage
from uuid import uuid1
from datetime import datetime as dt
from time import strftime
# DBM = lambda :TinyDB(storage=MemoryStorage)
import matplotlib.pyplot as plt

JSONDB = os.path.dirname(__file__) + '/eica.json'

DBF = lambda: TinyDB(JSONDB)
__author__ = 'carlo'

PONTOS = dict(_LINGUA_=120, _CHAVES_=130, _MUNDO_=140, _Chaves_=150, _ABAS_=110, _HOMEM_=90)
CARTAS = dict(fruta=142, objeto=144, animal=146, comida=148, arma=149, __A_T_I_V_A__=100)

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

    def new_merge_sessions_ordered(self, given_user):
        user_sessions = self.banco.search(self.query.user == given_user)
        value_keys = ("tempo", "carta", "casa", "valor", "ponto")
        tuple_session_values_content = [tuple([jogada[termo] for termo in value_keys])
                                        for sessions in user_sessions for jogada in sessions["jogada"]]
        sorted(tuple_session_values_content)
        dict_session_values = [{key: value for key, value in zip(value_keys, values)}
                               for values in tuple_session_values_content]
        return dict_session_values

    def new_merge_sessions_ordered(self, given_user):
        user_sessions = self.banco.search(self.query.user == given_user)
        value_keys = ("tempo", "carta", "casa", "valor", "ponto")
        tuple_session_values_content = [tuple([jogada[termo] for termo in value_keys])
                                        for sessions in user_sessions for jogada in sessions["jogada"]]
        sorted(tuple_session_values_content)
        dict_session_values = [{key: value for key, value in zip(value_keys, values)}
                               for values in tuple_session_values_content]
        return dict_session_values

    def merge_sessions_ordered(self, given_user):
        user_sessions = self.banco.search(self.query.value.user == given_user)
        value_keys = ("tempo", "carta", "casa", "valor", "ponto")
        tuple_session_values_content = [tuple([jogada[termo] for termo in value_keys])
                                        for sessions in user_sessions for jogada in sessions["value"]["jogada"]]
        sorted(tuple_session_values_content)
        dict_session_values = [{key: value for key, value in zip(value_keys, values)}
                               for values in tuple_session_values_content]
        return dict_session_values

    def caution_reformat_db_to_shallow_dict(self):
        def reformat_a_user(user):
            value_keys = ["user", "idade", "ano", "sexo", "jogada"]
            shallow_content = {key: user["value"][key] for key in value_keys}
            return shallow_content
        users = self.find_all_users()
        for user in users:
            self.banco.update(reformat_a_user(user), eids=[user.eid])
            self.banco.update(delete('value'), eids=[user.eid])

    def new_update_user_with_merged_data(self, given_user):
        raise()
        given_user_merged_dict_list = self.new_merge_sessions_ordered(given_user)
        user_sessions = self.banco.search(self.query.user == given_user)
        user_sessions[0]["jogada"] = given_user_merged_dict_list
        given_user_other_ids_to_be_removed = [session.eid for session in user_sessions[1:]]
        self.banco.remove(eids=given_user_other_ids_to_be_removed)
        return given_user_other_ids_to_be_removed

    def find_those_users(self, names):
        users = self.banco.search(self.query.value.user.exists())
        return [(a.eid, a["value"]["user"]) for a in users if a["value"]["user"] in names]

    def find_all_users_names(self):
        users = self.banco.search(self.query.value.user.exists())
        return [a["value"]["user"] for a in users]

    def new_find_all_users_names(self):
        users = self.banco.search(self.query.user.exists())
        return [a["user"] for a in users]

    def find_those_users_ids(self, names):
        users = self.banco.search(self.query.value.user.exists())
        return [a.eid for a in users if a["value"]["user"] in names]

    def new_find_inconsistent_users_ids(self, name):
        users = self.banco.search(self.query.user == name)
        dem = ["user", "idade", "sexo", "ano"]
        valueset = set(next(((d, val[d]) for d in dem) for val in list(users)))
        jogada = [item for sublist in users for item in sublist['jogada']]
        dados = {dado[0]: dado[1] if dado[0] != "idade" else int(dado[1].replace("anos", "")) + 5 for dado in valueset}
        # jogada = users[0]["value"]['jogada']

        dados.update(dict(hora=jogada[0]["tempo"] if jogada else 0))
        return dados

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
            tempo = dt.strptime(max(tempos).split(".")[0], timeformat)\
                - dt.strptime(min(tempos).split(".")[0], timeformat)
            print("{:3d}".format(i), "Lances: {:3d}".format(jogadas),
                  "T:{:>9}".format(str(tempo)), report.format(**name))

    def new_rename_users_across_days(self, users=('Tatiane Monteiro Nascimento', 'patrick de oliveira nascimento')):
        for user in users:
            eid_name_date = self.new_split_user_across_days(user)
            [self.banco.update(dict(user=date_name), eids=[date_eid]) for date_eid, date_name, _ in eid_name_date]

    def new_split_user_across_days(self, user):
        user_sessions = self.banco.search(self.query.user == user)
        dias = [user["jogada"][0]["tempo"].split()[0] for user in user_sessions if user["jogada"]]
        dias = set(dias)
        if len(dias) > 1:
            dias = [(user.eid, user["user"]+(str(dia) if dia else ""), data)
                    for user in user_sessions
                    for dia, data in enumerate(dias)
                    if user["jogada"] and user["jogada"][0]["tempo"].split()[0] == data]
        return dias

    def new_report_user_data(self):
        banco = self
        unique = set(banco.new_find_all_users_names())
        values = [banco.new_find_inconsistent_users_ids(name) for name in unique]
        values = [value for value in values if value["hora"] != 0]
        dem = ["user", "idade", "sexo", "ano", "hora"]
        valuetuple = [tuple(line[key] for key in dem) for line in values]
        valuetuple.sort(key=lambda tp: tp[0].lower().replace(" ", ""))
        values = [{key: value for key, value in zip(dem, line)} for line in valuetuple]
        report = "nome:{user: >40}  idade: {idade: >4}   ano: {ano}   dia+hora: {hora} genero: {sexo} "
        for i, name in enumerate(values):
            jogadas = sum(len(copy["jogada"])
                          for copy in self.banco.search(self.query.user == name["user"]))
            tempos = [copy["jogada"]
                      for copy in self.banco.search(self.query.user == name["user"])]
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

    def new_list_play_data_with_delta(self, u_name='wesleyana vitoria aquino de souza'):
        timeformat = "%Y-%m-%d %H:%M:%S.%f"
        # userdata = self.banco.search((self.query.user == u_name) and (self.query.jogada != []))
        # userdata = [data for user in userdata for data in user["jogada"]]
        userdata = self.new_merge_sessions_ordered(u_name)
        userdata = [userdata[0]]+userdata
        value_keys = ("tempo", "carta", "casa", "valor", "ponto", "delta")
        initial_time = dt.strptime(userdata[0]["tempo"], timeformat)
        options = {key: lambda _, data, k: data[k] for key in value_keys}

        def get_delta(i, *args):
            tempo = dt.strptime(userdata[i]["tempo"], timeformat)\
                - dt.strptime(userdata[i-1]["tempo"], timeformat)
            return tempo.total_seconds()

        def get_playtime(i, *args):
            timeformat = "%Y-%m-%d %H:%M:%S.%f"
            tempo = dt.strptime(userdata[i]["tempo"], timeformat)\
                - initial_time
            return tempo.total_seconds()
        options["delta"] = get_delta
        options["tempo"] = get_playtime
        playdata = [{key: options[key](i, data, key)
                     for key in value_keys} for i, data in enumerate(userdata[1:])]
        return playdata

    def simple_plot(self, data):
        def to_floatornan(number, ponto):
            try:
                return float(number)
            except ValueError:
                return -2.0

        def to_floatormarker(number, ponto):
                if number in "objeto fruta arma animal comida __A_T_I_V_A__".split():
                    if number == "__A_T_I_V_A__":
                        return -2.0
                    else:
                        return CARTAS[number]
                return -2.0

        def to_floatorgame(number, ponto):
            if number in "__A_T_I_V_A__":
                return PONTOS[ponto]
            return -2.0
        fig1 = plt.figure()
        x = [0] + [float(d["tempo"]) for d in data] + [float(data[-1]["tempo"]) + 1]

        y = [-2] + [to_floatornan(d["carta"], d["ponto"]) for d in data] + [-2]
        z = x[:]
        w = [-2] + [to_floatormarker(d["carta"], d["ponto"]) for d in data] + [-2]
        j = x[:]
        k = [-2] + [to_floatorgame(d["carta"], d["ponto"]) for d in data] + [-2]
        # l, = plt.plot([], [], 'r-')
        # plt.xlim(0, 1200)
        plt.ylim(0, 150)
        plt.xlabel('tempo')
        plt.title('wesley')
        plt.fill(z, w, 'b-', linewidth=0)
        plt.fill(j, k, 'g', linewidth=0)
        plt.fill(x, y, 'r-', linewidth=0)
        # plt.bar(x, y, 'r', linewidth=2)
        # plt.bar(z, w, 'b', linewidth=2)
        # plt.bar(j, k, 'g', linewidth=2)
        # plt.barh(y_pos, performance, align='center', alpha=0.4)

        plt.grid(True)

        # line, = plt.plot(x, y, '-')

        dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off
        # line.set_dashes(dashes)

        plt.show()

    def save(self, value):
        key = str(uuid1())
        self.banco.insert(dict(key=key, value=value))
        return key


if __name__ == '__main__':
    banco = Banco()
    prin = banco.new_find_all_users_names()
    banco.new_report_user_data()
    banco.simple_plot(banco.new_list_play_data_with_delta())  # "Pitter Guimaraes Correia Goncalves"))
    for i in banco.new_list_play_data_with_delta():  # ("Pitter Guimaraes Correia Goncalves"):
        print(i)
    # banco.report_user_data()
    # banco.report_no_user_data()
    # banco.rename_user_with_inconsistent_names()

