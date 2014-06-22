# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime
from google.appengine.ext import ndb


class Gasto(ndb.Model):
    descricao = ndb.StringProperty(required=True)
    valor = ndb.FloatProperty(required=True)
    data = ndb.DateTimeProperty(auto_now_add=True)
    data_informada = ndb.DateProperty()

    def to_dict(self):
        dct=super(Gasto, self).to_dict()
        dct['data']=self.data.strftime('%d/%m/%Y')
        dct['data_informada']=self.data_informada.strftime('%d/%m/%Y')
        dct['id']=self.key.id()
        return dct


def index(_json):
    query = Gasto.query().order(Gasto.data)
    gastos = query.fetch()
    gastos_lista_dct=[g.to_dict() for g in gastos]
    _json(gastos_lista_dct)


def salvar(_json,descricao, valor, data_informada):
    data = datetime.datetime.strptime(data_informada, '%d/%m/%Y')
    valor = float(valor)
    gasto = Gasto(descricao=descricao, valor=valor, data_informada=data)
    gasto.put()
    _json(gasto.to_dict())


def apagar(gasto_id):
    chave = ndb.Key(Gasto, int(gasto_id))
    chave.delete()


def atualizar(gasto_id, descricao=None, valor=None, data_informada=None):
    gasto_id = int(gasto_id)
    gasto = Gasto.get_by_id(gasto_id)
    if descricao is not None:
        gasto.descricao = descricao
    if descricao is not None:
        gasto.valor = float(valor)
    if data_informada is not None:
        data = datetime.datetime.strptime(data_informada, '%d/%m/%Y')
        gasto.data_informada=data
    gasto.put()




