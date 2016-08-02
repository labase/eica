# -*- coding: UTF8 -*-
__author__ = 'carlo'
from datetime import datetime
from bottle import default_app, route, view, get, post, static_file, request, redirect, run, TEMPLATE_PATH
import os
import modelo as database
import json

DIR = os.path.dirname(__file__)  # + '/view'
INDEX = os.path.dirname(__file__) + '/../'
LAST = None
PEC = "jogada"
HEAD = "carta casa move tempo ponto valor".split()
FAKE = [{k: 10 * i + j for j, k in enumerate(HEAD)} for i in range(4)]


def retrieve_data(req):
    jdata = req['data']
    print (jdata)
    return json.loads(jdata)


def retrieve_params(req):
    # print ('retrieve_params', req)
    doc_id = req.pop('doc_id')
    data = {k: req[k] for k in req}
    print (doc_id, data)
    return {doc_id: data}


@route('/')
def hello_world():
    # redirect('/carinhas/carinhas.html')
    # redirect('/tuple/index.html')
    redirect("/static/index.html")


@route('/ei')
def go_eica():
    # redirect('/carinhas/carinhas.html')
    # redirect('/tuple/index.html')
    redirect('/eica/test.html')


@route('/ei')
def go_eica():
    # redirect('/carinhas/carinhas.html')
    # redirect('/tuple/index.html')
    redirect('/eica/test.html')


@get('/static/<filename:re:.*\.css>')
def stylecss(filename):
    # print('/static/<filename:re:.*\.css>', filename, INDEX)
    return static_file(filename, root=DIR + "/views")


@get('/static/<filename:re:.*\.(html|py)>')
def code(filename):
    # print('/static/<filename:re:.*\.css>', filename, INDEX)
    return static_file(filename, root=INDEX)


@get('/record/getid')
def get_user_id_():
    global LAST
    gid = database.DRECORD.save({PEC: []})
    print('/record/getid', gid)
    LAST = gid
    return gid


@get('/pontos')
@view('resultado')
def score():
    try:
        record_id = LAST
        if record_id is None:
            raise Exception()
        # print('resultado', record_id)
        record = database.DRECORD[record_id]
        record = record[PEC]
        # print('record resultado:', record)
        return dict(user=record_id, result=record)
    except Exception:
        # return dict(user="FAKE", result=FAKE)
        fake = dict(user="FAKE", result=FAKE)
        # print('score', fake)
        return fake


@post('/record/store')
def store():
    try:
        jsondata = retrieve_params(request.params)
        record_id = jsondata.keys()[0]
        record = database.DRECORD[record_id]
        score = jsondata[record_id]
        # print('record/store:', score, record)
        score["tempo"] = str(datetime.now())
        record[PEC] += [score]
        # print('record score:', score, record)
        database.DRECORD[record_id] = record
        return record
    except Exception:
        return "Movimento de peça não foi gravado %s" % str(request.params.values())


application = default_app()

if __name__ == "__main__":
    TEMPLATE_PATH.insert(0, DIR)
    run(host='localhost', port=8080)
