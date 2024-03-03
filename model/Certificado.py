# -*- coding: utf-8 -*-
import datetime


class Certificado:

    def __init__(
            self, nome_fantasia='', nome_divulgacao='', segmento='', cidade='', uf='',
            retroativos=None, telefone='', preco='', obs='', tipo='', ano=None
    ):
        if retroativos is None:
            retroativos = []
        self.nome_fantasia = nome_fantasia
        self.nome_divulgacao = nome_divulgacao
        self.segmento = segmento
        self.cidade = cidade
        self.uf = uf
        self.telefone = telefone
        self.preco = preco
        self.obs = obs
        self.tipo = tipo
        self.retroativos = retroativos

        if ano is None:
            self.ano = str(datetime.datetime.now().year)
        else:
            self.ano = ano
