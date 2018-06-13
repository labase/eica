#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Carinhas
# Copyright 2013-2014 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Carinhas é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser  útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
#  a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, escreva para a Fundação do Software
# Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
############################################################
SuperPython - Teste de Funcionalidade Web
############################################################

Verifica a funcionalidade do servidor web.

"""
__author__ = 'carlo'
import unittest
import sys

import bottle
import os
import sys
import os

project_server = os.path.dirname(os.path.abspath(__file__))
project_server = os.path.join(project_server, '../src/')
# print(project_server)
sys.path.insert(0, project_server)
# make sure the default templates directory is known to Bottle
templates_dir = os.path.join(project_server, 'server/views/')
# print(templates_dir)
if templates_dir not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, templates_dir)
if sys.version_info[0] == 2:
    from mock import MagicMock, patch
else:
    from unittest.mock import MagicMock, patch, ANY
from webtest import TestApp
from server.control import application as appbottle
import server.modelo as cs
import server.control as ct


class SpyWebTest(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(name="db")
        modules = {
            'server.modelo': self.db,
            'server.modelo.DRECORD': self.db
        }
        self.module_patcher = patch.dict('sys.modules', modules)
        self.module_patcher.start()
        cs.DRECORD = MagicMock(name="sdb")
        pass

    def test_default_page(self):
        app = TestApp(appbottle)
        response = app.get('/static/index.html')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('<title>Jogo Eica - Cadastro</title>' in response.text, response.text[:1000])

    def test_default_redirect(self):
        app = TestApp(appbottle)
        response = app.get('/')
        self.assertEqual('302 Found', response.status)

    def test_register(self):
        app = TestApp(appbottle)
        cs.DRECORD.save = MagicMock(name="dbl", return_value='projeto2222-lastcodename')
        response = app.get('/static/register?doc_id="10000001"&module="projeto2222"')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('projeto2222-lastcodename' in response, str(response))
        cs.DRECORD.save.assert_called_once_with({'module': '"projeto2222"', 'jogada': []})

    def test_store(self):
        app = TestApp(appbottle)
        cs.DRECORD.save = MagicMock(name="dbl", return_value='projeto2222-lastcodename')
        cs.DRECORD.get = MagicMock(name="dblg", return_value={'doc_id': 'projeto2222-lastcodename', 'jogada': []})
        cs.DRECORD.set = MagicMock(name="dbls")
        response = app.post('/record/store', dict(doc_id="10000001", module="projeto2222"))
        self.assertEqual('200 OK', response.status)
        self.assertTrue('projeto2222-lastcodename' in response, str(response))
        self.assertTrue('"jogada": [{"module": "projeto2222", "tempo": "20' in response, str(response))
        cs.DRECORD.set.assert_called_once_with('10000001', ANY)

    def test_pontos(self):
        ct.LAST = "10000001"
        app = TestApp(appbottle)
        jogada = {"carta": 2222,
                  "casa": 2222,
                  "move": 2222,
                  "ponto": 2222,
                  "tempo": 2222,
                  "valor": 2222}

        user, idade, ano, sexo, result = 'projeto2222-lastcodename', '00015', '0009', 'sexo', dict(doc_id="10000001", jogada=[jogada])
        user_data = dict(user=user, idade=idade, ano=ano, sexo=sexo, jogada=[jogada])
        cs.DRECORD.get = MagicMock(name="dblg", return_value=user_data)
        response = app.get('/pontos')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('projeto2222-lastcodename' in response, str(response))
        self.assertTrue('<h3>Idade: 10 Genero: sexo Ano Escolar: 9</h3>' in response, str(response))
        cs.DRECORD.get.assert_called_once_with('10000001')

    def _test_save(self):
        app = TestApp(appbottle)
        session = MagicMock(name="dblc")
        session.name = '2222'
        cs.DB.login = MagicMock(name="dbl")
        cs.DB.login.side_effect = lambda *a, **args: (session, 1)
        cs.DB.save = MagicMock(name="dblc")
        cs.DB.save.side_effect = lambda *a, **args: 'lastcodename lastcodetext'.split()
        response = app.post_json('/main/save', dict(person="projeto0", name="main", text="# main"))
        cs.DB.save.assert_called_once_with(text=u'# main', name=u'main', person=u'projeto0')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('main' in response.text, response.text)

    def _test_import(self):
        app = TestApp(appbottle)
        session = MagicMock(name="dblc")
        session.name = '2222'
        cs.DB.load = MagicMock(name="dbl")
        cs.DB.load.side_effect = lambda *a, **args: "#main"
        response = app.get('/main/superpython/core.py')
        cs.DB.load.assert_called_once_with(name='core.py')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('#main' in response)

    def _test_logout(self):
        app = TestApp(appbottle)
        session = MagicMock(name="dblc")
        session.name = '2222'
        cs.DB.logout = MagicMock(name="dbl")
        # cs.DB.load.side_effect = lambda *a, **args: "#main"
        response = app.post('/main/logout', dict(person="projeto2222"))
        cs.DB.logout.assert_called_once_with('superpython', 'projeto2222')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('logout' in response)


if __name__ == '__main__':
    unittest.main()
