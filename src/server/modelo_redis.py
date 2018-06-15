#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa EICA
# Copyright 2014-2017 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://j.mp/GNU_GPL3>`__.
#
# EICA é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

"""Redis database Model.

.. moduleauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

"""
from redislite import Redis
from uuid import uuid1
from json import loads
from json import dumps
__author__ = 'carlo'
# JSONDB = os.path.dirname(__file__) + '/eica.db'
JSONDB = '/home/carlo/eica.db'


def _get_redis(db=JSONDB):
    return Redis(db)


DBF = _get_redis


class Banco:
    def __init__(self, base=DBF):
        self.banco = base()

    def save(self, value):
        key = str(uuid1())
        self.set(key, value)
        return key

    def get(self, key):
        return loads(self.banco.get(key).decode('utf8'))

    def set(self, key, value):
        self.banco.set(key, dumps(value))
        return key


DBT = lambda: Redis('/tmp/redis.db')


def tests():

    b = Banco(DBT)
    b.set(1, 2)
    assert int(b.get(1)) == 2, "falhou em recuperar b[1]: %s" % str(b.get(1))
    print("assert b.get(1) == 2", str(b.get(1)))
    b.set(1, 3)
    assert int(b.get(1)) == 3, "falhou em recuperar b[1]: %s" % str(b.get(1))
    c = b.save('oi maçã')
    assert b.get(c) == 'oi maçã', "falhou em recuperar b[1]: %s" % str(b.get(c))


if __name__ == "__main__":
    tests()
else:
    DRECORD = Banco()
