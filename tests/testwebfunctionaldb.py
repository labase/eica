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
import server.modelo_redis as cs
import server.control as ct


class FunctionalWebTest(unittest.TestCase):
    def setUp(self):
        cs.DBF = '/tmp/redis_test.db'
        pass

    def test_default_page(self):
        """ test_default_page """
        app = TestApp(appbottle)
        response = app.get('/static/index.html')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('<title>Jogo Eica - Cadastro</title>' in response.text, response.text[:1000])

    def test_default_redirect(self):
        """test_default_redirect  """
        app = TestApp(appbottle)
        response = app.get('/')
        self.assertEqual('302 Found', response.status)

    def test_register(self):
        """test_register  """
        app = TestApp(appbottle)
        response = app.get('/static/register?doc_id="10000001"&module=projeto2222')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('be9c-e0cb4e39e071' in response, str(response))
        rec_id = str(response).split('ver = main("')[1].split('e0cb4e39e071")')[0] + 'e0cb4e39e071'
        assert cs.DRECORD.get(rec_id) == "{'module': 'projeto2222', 'jogada': []}", "{}: {}".format(rec_id, cs.DRECORD.get(rec_id))

    def test_store(self):
        """test_store  """
        app = TestApp(appbottle)
        response = app.post('/record/store', dict(doc_id="10000001", module="projeto2222"))
        self.assertEqual('200 OK', response.status)
        self.assertTrue('projeto2222-lastcodename' in response, str(response))
        self.assertTrue('"jogada": [{"module": "projeto2222", "tempo": "20' in response, str(response))

    def _test_pontos(self):
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
        response = app.get('/pontos')
        self.assertEqual('200 OK', response.status)
        self.assertTrue('projeto2222-lastcodename' in response, str(response))
        self.assertTrue('<h3>Idade: 10 Genero: sexo Ano Escolar: 9</h3>' in response, str(response))
        cs.DRECORD.get.assert_called_once_with('10000001')


if __name__ == '__main__':
    unittest.main()
