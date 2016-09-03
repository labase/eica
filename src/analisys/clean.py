# -*- coding: UTF8 -*-
from tinydb import TinyDB, Query
from tinydb.operations import delete
import os
import operator
# from tinydb.storages import MemoryStorage
from uuid import uuid1
from datetime import datetime as dt
from datetime import timedelta as td
import matplotlib.pyplot as plt

Y_M_D_H_M_S = "%Y-%m-%d %H:%M:%S"

JSONDB = os.path.dirname(__file__) + '/eica.json'
JSONDBOUT = os.path.dirname(__file__) + '/eica_new.json'

DBF = lambda: TinyDB(JSONDB)
__author__ = 'carlo'

PONTOS = dict(_LINGUA_=120, _CHAVES_=130, _MUNDO_=140, _Chaves_=150, _ABAS_=110, _HOMEM_=90)
PONTO = "_LINGUA_ _CHAVES_ _MUNDO_ _Chaves_ _ABAS_ _FALA_ _Mundo_ _HOMEM_".split()
CARTAS = dict(fruta=142, objeto=144, animal=146, comida=148, arma=149, __A_T_I_V_A__=100)
FILTRO = dict(
    _LINGUA_=lambda item, casa, ponto, valor, plot: [55, 60][bool(valor)] if plot == "_LINGUA_" else -2,
    _CHAVES_=lambda item, casa, ponto, valor, plot: [65, 70][bool(valor)] if plot == "_CHAVES_" else -2,
    _MUNDO_=lambda item, casa, ponto, valor, plot: [75, 80][bool(valor)] if plot == "_MUNDO_" else -2,
    _Chaves_=lambda item, casa, ponto, valor, plot: item if plot == "_Chaves_" else -2,
    _ABAS_=lambda item, casa, ponto, valor, plot: int(casa.split("_")[0]) // 10 if plot == "_ABAS_" else -2,
    _HOMEM_=lambda item, casa, ponto, valor, plot: [85, 90][bool(valor)] if plot == "_HOMEM_" else -2,
    _FALA_=lambda item, casa, ponto, valor, plot:
    sum(int(val) for val in item.split("_")) // 2 if plot == "_FALA_" else -2,
    _Mundo_=lambda item, casa, ponto, valor, plot: item if plot == "_Mundo_" else -2,
)
nousers = "carlo,carla,Jonatas,ggggg,,Jonatas Rafael,JonatasRafael,Rafael,Gabriel,teste,Camila (teste)".split(",")

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

SB = "TATIANE MONTEIRO|R|ALTA|VERDADEIRO SUCESSO|TONI CARLOS|R|ZERO|FALSO SUCESSO|KAYKE|R|ZERO|FALSO SUCESSO|" \
     "ANICOLER|I|ZERO|ALTA DOTAÇÂO|ISRAEL|B|BAIXA|ALTA DOTAÇÂO|CASSIANA VENTURA|I|ZERO|ALTA DOTAÇÂO|" \
     "MARIA EDUARDA ALVES|I|ZERO|EXPULSÃO SIMBÓLICA|RADAMES|B|BAIXA|FALSO SUCESSO|ESTER|I|ZERO|EXPULSÃO SIMBÓLICA|" \
     "KEYLA|I|BAIXA|EXPULSÃO SIMBÓLICA|CHRISTIAN|R|ZERO|FALSO SUCESSO|ANTONIOGUILHERME|R|BAIXA|FALSO SUCESSO|" \
     "ANA FERNANDA|R|MÉDIA|SUCESSO MÍNIMO|MARIA EDUARDA DA SILVA|I|BAIXA|EXPULSÃO SIMBÓLICA|PATRICK|B|MÉDIA|" \
     "SUCESSO MÍNIMO|SAMUEL|B|BOA|VERDADEIRO SUCESSO|PITTER|B|ALTA|VERDADEIRO SUCESSO|LINDA|R|ALTA|" \
     "VERDADEIRO SUCESSO|JULIA|I|BAIXA|EXPULSÃO SIMBÓLICA|KAUE|R|ALTA|VERDADEIRO SUCESSO|RENAN|R|ALTA|" \
     "VERDADEIRO SUCESSO|THIAGO|R|BOA|VERDADEIRO SUCESSO|FILIPE|R|BAIXA|FALSO SUCESSO|LAIZA|R|ALTA|" \
     "VERDADEIRO SUCESSO|JULIE BRENDA|R|ALTA|VERDADEIRO SUCESSO|KAMILLE|R|ALTA|VERDADEIRO SUCESSO|" \
     "WESLEYANA|R|ALTA|ALTA DOTAÇÂO|LETICIA|I|ZERO|ALTA DOTAÇÂO|".split("|")
TB = "TATIANE MONTEIRO|R|ALTA|VERDADEIRO SUCESSO|TONI CARLOS|R|ZERO|FALSO SUCESSO|KAYKE|R|ZERO|FALSO SUCESSO|" \
     "MARIA EDUARDA ALVES|I|ZERO|EXPULSÃO SIMBÓLICA|RADAMES|B|BAIXA|FALSO SUCESSO|ESTER|I|ZERO|EXPULSÃO SIMBÓLICA|" \
     "KEYLA|I|BAIXA|EXPULSÃO SIMBÓLICA|CHRISTIAN|R|ZERO|FALSO SUCESSO|ANTONIOGUILHERME|R|BAIXA|FALSO SUCESSO|" \
     "ANA FERNANDA|R|MÉDIA|SUCESSO MÍNIMO|MARIA EDUARDA DA SILVA|I|BAIXA|EXPULSÃO SIMBÓLICA|PATRICK|B|MÉDIA|" \
     "SUCESSO MÍNIMO|SAMUEL|B|BOA|VERDADEIRO SUCESSO|PITTER|B|ALTA|VERDADEIRO SUCESSO|LINDA|R|ALTA|" \
     "VERDADEIRO SUCESSO|JULIA|I|BAIXA|EXPULSÃO SIMBÓLICA|KAUE|R|ALTA|VERDADEIRO SUCESSO|RENAN|R|ALTA|" \
     "VERDADEIRO SUCESSO|THIAGO|R|BOA|VERDADEIRO SUCESSO|FILIPE|R|BAIXA|FALSO SUCESSO|LAIZA|R|ALTA|" \
     "VERDADEIRO SUCESSO|JULIE BRENDA|R|ALTA|VERDADEIRO SUCESSO|KAMILLE|R|ALTA|VERDADEIRO SUCESSO|" \
     "WESLEYANA|R|ALTA|VERDADEIRO SUCESSO|".split("|")


class Banco:
    def __init__(self, base=DBF):
        self.banco = base()
        self.query = Query()
        self.users = []
        self.initial_time = 0

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

    def new_list_play_data_adjusted_with_delta(self, given_user):
        timeformat = "%Y-%m-%d %H:%M:%S.%f"
        user_sessions = self.banco.search(self.query.user == given_user)
        # print(len(user_sessions), next(s["jogada"][0] if s["jogada"] else "######" for s in user_sessions))
        tuple_session_values_content = [(jogada.update({0: i}) if i == 0 else 0, jogada)[1]
                                        for sessions in user_sessions for i, jogada in enumerate(sessions["jogada"])
                                        if sessions["jogada"]]
        tuple_session_values_content.sort(key=operator.itemgetter("tempo"))

        self.initial_time = dt.strptime(tuple_session_values_content[0]["tempo"], timeformat)
        all_plays = zip(tuple_session_values_content, tuple_session_values_content[1:])

        def calc(antjog, jog):
            # print(antjog)
            last_play_time = dt.strptime(antjog["tempo"], timeformat)
            delta = dt.strptime(jog["tempo"], timeformat) - last_play_time
            if 0 in jog:
                self.initial_time += delta - td(seconds=1)
                delta = td(seconds=1)
                # jog.pop(0)
            tempo = dt.strptime(jog["tempo"], timeformat) - self.initial_time
            jog = dict(jog)

            jog.update(dict(tempo=tempo.total_seconds(), delta=delta.total_seconds()))
            return jog

        first = tuple_session_values_content
        first = calc(first[0], first[0])

        merge = [first] + [calc(antjog, jog) for antjog, jog in all_plays]
        # for pl in merge:
        #     print("tempo ", pl["tempo"], "  delta", pl["delta"], "XXXXXXXXXX" if 0 in pl else "")
        return merge

    def new_merge_timed_sessions_ordered(self, given_user):
        user_sessions = self.banco.search(self.query.user == given_user)
        value_keys = ("tempo", "carta", "casa", "valor", "ponto")
        tuple_session_values_content = [tuple([jogada["tempo"], jogada])
                                        for sessions in user_sessions for jogada in sessions["jogada"]]
        tuple_session_values_content.sort(key=operator.itemgetter(0))
        dict_session_values = [values[1]
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
        def reformat_a_user(usr):
            value_keys = ["user", "idade", "ano", "sexo", "jogada"]
            shallow_content = {key: usr["value"][key] for key in value_keys}
            return shallow_content

        users = self.find_all_users()
        for user in users:
            self.banco.update(reformat_a_user(user), eids=[user.eid])
            self.banco.update(delete('value'), eids=[user.eid])

    def new_update_user_with_merged_data(self, given_user):
        pass
        """
        given_user_merged_dict_list = self.new_merge_sessions_ordered(given_user)
        user_sessions = self.banco.search(self.query.user == given_user)
        user_sessions[0]["jogada"] = given_user_merged_dict_list
        given_user_other_ids_to_be_removed = [session.eid for session in user_sessions[1:]]
        self.banco.remove(eids=given_user_other_ids_to_be_removed)
        return given_user_other_ids_to_be_removed"""

    def find_those_users(self, names):
        users = self.banco.search(self.query.value.user.exists())
        return [(a.eid, a["value"]["user"]) for a in users if a["value"]["user"] in names]

    def find_all_users_names(self):
        users = self.banco.search(self.query.value.user.exists())
        return [a["value"]["user"] for a in users]

    def new_find_all_users_names(self):
        users = self.banco.search(self.query.user.exists())
        return [a["user"] for a in users if self.new_merge_timed_sessions_ordered(a["user"])]

    def new_find_those_users_ids(self, names):
        users = self.banco.search(self.query.user.exists())
        return [a.eid for a in users if a["user"] in names]

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
        values = [value for value in values
                  if value["hora"] == 0 and value["user"] not in nousers]
        report = "nome:{user: >40}  idade: {idade: >4}   ano: {ano}   dia+hora: {hora} genero: {sexo} "
        for i, name in enumerate(values):
            print("{:3d}".format(i), report.format(**name))

    def report_user_data(self, desde="2016-08-08 00:00:0.0"):
        timeformat = "%Y-%m-%d %H:%M:%S.%f"
        banco = self
        desde = dt.strptime(desde, timeformat)
        unique = set(banco.find_all_users_names())
        unique -= set(nousers)
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
            if dt.strptime(tempos[0], timeformat) < desde:
                continue
            # tempo = strptime(max(tempos), "%c")-strptime(min(tempos), "%c")
            tempo = dt.strptime(max(tempos), timeformat) \
                    - dt.strptime(min(tempos), timeformat)
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
            dias = [(user.eid, user["user"] + (str(dia) if dia else ""), data)
                    for user in user_sessions
                    for dia, data in enumerate(dias)
                    if user["jogada"] and user["jogada"][0]["tempo"].split()[0] == data]
        return dias

    def new_report_user_data(self):
        banco = self
        unique = set(banco.new_find_all_users_names()) - set(nousers)
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
            timeformat = Y_M_D_H_M_S
            tempo = dt.strptime(max(tempos).split(".")[0], timeformat) \
                    - dt.strptime(min(tempos).split(".")[0], timeformat)
            print("{:3d}".format(i), "Lances: {:4d}".format(jogadas),
                  "T:{:>9}".format(str(tempo)), report.format(**name))

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

    def new_rename_user_with_inconsistent_names(self):
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
            allcopies = [(master, record.eid, record["user"])
                         for u_name in user
                         for record in self.banco.search(self.query.user == u_name)]
            # print(allcopies)
            for _, oid, name in allcopies:
                self.banco.update(dict(user=master), eids=[oid])

    def report_merged_user(self, user="tatiane monteiro nascimento"):
        merge_sorted_data = self.merge_sessions_ordered(user)
        for i, data in enumerate(merge_sorted_data):
            print(i, data)
            # print(i, "nome:{user: >40}  idade: {idade: >4}   ano: {ano}     genero: {sexo}".format(**name))

    def new_list_play_data_with_delta(self, u_name='wesleyana vitoria aquino de souza'):
        timeformat = "%Y-%m-%d %H:%M:%S.%f"
        # userdata = self.banco.search((self.query.user == u_name) and (self.query.jogada != []))
        # userdata = [data for user in userdata for data in user["jogada"]]
        userdata = self.new_merge_timed_sessions_ordered(u_name)
        userdata = [userdata[0]] + userdata
        value_keys = ("tempo", "carta", "casa", "valor", "ponto", "delta")
        initial_time = dt.strptime(userdata[0]["tempo"], timeformat)
        options = {key: lambda _, data, k: data[k] for key in value_keys}

        def get_delta(i, *args):
            tempo = dt.strptime(userdata[i]["tempo"], timeformat) \
                    - dt.strptime(userdata[i - 1]["tempo"], timeformat)
            return tempo.total_seconds()

        def get_playtime(i, *args):
            timeformat = "%Y-%m-%d %H:%M:%S.%f"
            tempo = dt.strptime(userdata[i]["tempo"], timeformat) \
                    - initial_time
            return tempo.total_seconds()

        options["delta"] = get_delta
        options["tempo"] = get_playtime
        playdata = [{key: options[key](i, data, key)
                     for key in value_keys} for i, data in enumerate(userdata[1:])]
        return playdata

    def __new_list_play_data_adjusted_with_delta(self, u_name='wesleyana vitoria aquino de souza'):
        timeformat = "%Y-%m-%d %H:%M:%S.%f"
        userdata = self.new_merge_adjusted_timed_sessions_ordered(u_name)
        userdata = [userdata[0]] + userdata
        value_keys = ("tempo", "carta", "casa", "valor", "ponto", "delta")
        initial_time = dt.strptime(userdata[0][1][0]["tempo"], timeformat)
        options = {key: lambda _, j, data, k: data[k] for key in value_keys}

        def get_delta(i, *args):
            tempo = dt.strptime(userdata[i]["tempo"], timeformat) \
                    - dt.strptime(userdata[i - 1]["tempo"], timeformat)
            return tempo.total_seconds()

        def get_playtime(i, j, *args):
            timeformat = "%Y-%m-%d %H:%M:%S.%f"
            tempo = dt.strptime(userdata[i]["tempo"], timeformat) \
                    - initial_time - j
            return tempo.total_seconds()

        options["delta"] = get_delta
        options["tempo"] = get_playtime
        playdata = [{key: options[key](i, j, data, key)
                     for key in value_keys} for j, session in userdata for i, data in enumerate(session)]
        return playdata[1:]

    def new_simple_plot(self, u_name='wesleyana vitoria aquino de souza'):
        data = banco.new_list_play_data_with_delta(u_name)
        fig1 = plt.figure()
        x = [0.] + [float(d["tempo"]) for d in data] + [float(data[-1]["tempo"]) + 1]
        plt.ylim(0, 90)
        plt.xlabel('tempo')
        plt.title(u_name)
        plt.gca().set_color_cycle(['red', 'green', 'blue', "orange", "magenta", "cyan", "black", 'yellow'])
        for plot in PONTO:
            plt.fill(x, [-2] + [FILTRO[d["ponto"]](d["carta"], d["casa"], d["ponto"], d["valor"], plot)
                                for d in data] + [-2], linewidth=0)
        plt.legend([plot for plot in PONTO], ncol=4, bbox_to_anchor=(0, 1, 1, 3),
                   loc=3, borderaxespad=1.2, mode="expand", )
        plt.grid(True)
        plt.subplots_adjust(bottom=0.08, left=.05, right=.96, top=.8, hspace=.35)
        fig1.savefig("plot/%s.jpg" % "_".join(u_name.split()))

        # plt.show()

    def parse_prognostics(self):
        prog = "EXPULSÃO SIMBÓLICA,FALSO SUCESSO,SUCESSO MÍNIMO,VERDADEIRO SUCESSO".split(",")
        tt = "nome nota trans prog".split()
        ntb = zip(*[TB[i:-1:4] for i in range(4)])
        # ntb = zip(tb[0:], tb[1:], tb[2:], tb[3:])
        # print(list(next(ntb) for i in range(6)))
        prognostic_list = [{i[0]: i[1] if i[0] != "prog" else i[1][0] for i in zip(tt, tl)} for tl in ntb]
        # print(len(dtb))
        nm = set(n.lower() for n in Banco().new_find_all_users_names())

        def match(n):
            for entry in prognostic_list:
                if entry["nome"].lower() in n.lower():
                    return {key: entry[key] for key in tt[1:]}
            return {key: None for key in tt[1:]}

        user_prog_dict = {key.lower(): match(key) for key in nm}
        print(nm)

        for l in user_prog_dict:
            print(l, user_prog_dict[l])
        return user_prog_dict

    def new_use_once_only_clean_db_with_merged_sessions_and_prognostics(self):
        new_data_base = TinyDB(JSONDBOUT)
        prognostics = self.parse_prognostics()
        users_with_demographics = list(set(n for n in self.new_find_all_users_names()))
        new_user_list = [dict(
            jogada=self.new_list_play_data_adjusted_with_delta(user),
            **prognostics[user.lower()],
            **self.new_find_inconsistent_users_ids(user)
        ) for user in users_with_demographics]
        for user in new_user_list:
            print({key: val if key != "jogada" else val[0] for key, val in user.items()})
            new_data_base.insert(user)

        return new_user_list

    def script_to_provide_clean_db_from_zero(self):
        self.caution_reformat_db_to_shallow_dict()
        print(self.new_find_those_users_ids(nousers))
        self.use_with_caution_removes_records_fro_db(self.new_find_those_users_ids(nousers))
        self.new_rename_user_with_inconsistent_names()
        self.new_rename_users_across_days()
        self.new_use_once_only_clean_db_with_merged_sessions_and_prognostics()
        self.new_report_user_data()

    def save(self, value):
        key = str(uuid1())
        self.banco.insert(dict(key=key, value=value))
        return key


if __name__ == '__main__':
    banco = Banco()
    print(len(banco.find_all_users()))
    banco.script_to_provide_clean_db_from_zero()
    # prin = list(set(banco.new_find_all_users_names()))
    # banco.report_no_user_data()
    # exit()
    # for user in prin:
    #     banco.new_simple_plot(user)
    #################################################
    # banco.new_report_user_data()
    # banco.new_simple_plot()
    # for i in banco.new_list_play_data_with_delta():
    #     print(i)
    # banco.report_user_data()
    # banco.report_no_user_data()
    # banco.rename_user_with_inconsistent_names()
# Banco().parse_prognostics()
# Banco().new_clean_db_with_merged_sessions_and_prognostics()
