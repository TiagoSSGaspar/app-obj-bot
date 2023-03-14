import json
from model.Certificado import Certificado
from utils.DesenhaCertificado import DesenhaCertificado


def config_cert() -> list:
    with open('./utils/config_cert.json') as config_json:
        config_certificado = json.load(config_json)
        return config_certificado

def certs() -> list:
    with open('./utils/cert.json') as config_json:
        config_certificado = json.load(config_json)
        return config_certificado

def process_certificado_step():
    users = certs()
    c = 0
    for obj in users:
        cert = Certificado(
            obj['empresa'],
            obj['nomeDivulgacao'],
            obj['segmento'],
            obj['cidade'],
            obj['uf'],
        )
        draw = DesenhaCertificado(cert, config_cert())
        draw.criar_certificado()
        c += 1
        print(c)


from docx import Document

documento = Document()


def process_lista():
    users = certs()
    c = 0
    for obj in users:
        empresa = obj['empresa']
        segmento = obj['segmento']
        nome_divulgacao = obj['nomeDivulgacao']
        preco = obj['preco']
        if nome_divulgacao != '':
            empresa = nome_divulgacao

        text = '{} = {} '.format(segmento, empresa)

        paragrafo = documento.add_paragraph()
        paragrafo.add_run(text).bold = True

    documento.save('lista-divulgacao.docx')

process_lista()
