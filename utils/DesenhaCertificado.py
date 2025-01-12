# -*- coding: utf-8 -*-
import datetime
import random

from PIL import Image, ImageDraw, ImageFont

from model import Certificado

font = ImageFont.truetype(font="Microdot.ttf", size=200)


class DesenhaCertificado:

    def __init__(self, certificado: Certificado, config_certificado=None):
        if config_certificado is None:
            config_certificado = []
        self.certificado = certificado
        if certificado.ano in ["2024", "2025"]:
            self.cor_texto = (0, 0, 0, 255)
        else:
            self.cor_texto = (255, 255, 255, 255)
        self.config_certificado = config_certificado
        self.opcoes = {}

        if str(self.certificado.ano) == str(datetime.datetime.now().year):
            self.opcoes = self.procurar_config('default')
        elif str(self.certificado.ano) == '2022':
            self.opcoes = self.procurar_config('2022')
        elif str(self.certificado.ano) == '2023':
            self.opcoes = self.procurar_config('2023')
        else:
            self.opcoes = self.procurar_config('retroativo')

    def procurar_config(self, nome_config: str) -> dict:
        for config in self.config_certificado:
            if config['opcao'] == nome_config:
                return config

    def criar_nova_img(self, tamanho_img=(100, 100)) -> Image:
        altura_largura_img = font.getsize(str(tamanho_img).upper())
        img = Image.new("RGBA", altura_largura_img, 0)
        return img

    def escreve_img(self, texto_img: str = '') -> Image:
        nova_img = self.criar_nova_img(texto_img)
        draw = ImageDraw.Draw(nova_img, "RGBA")
        draw.text((18, 0), str(texto_img).upper(), self.cor_texto, font, stroke_width=2, stroke_fill='black')

        return nova_img

    def criar_certificado(self, modo_bot: bool = True) -> Image:
        tamanho_texto_empresa = tuple(self.opcoes['TAMANHO_TEXTO_EMPRESA'])
        tamanho_texto_segmento = tuple(self.opcoes['TAMANHO_TEXTO_SEGMENTO'])
        tamanho_texto_cidade_uf = tuple(self.opcoes['TAMANHO_TEXTO_CIDADE_UF'])

        xy_cidade_uf_empresa = None

        if not str(self.certificado.ano) in ['2022', '2023', '2024', str(datetime.datetime.now().year)]:
            for opcao in self.opcoes['XY_CIDADE_UF_EMPRESA']:
                if str(self.certificado.ano) == opcao['ano']:
                    xy_cidade_uf_empresa = tuple(opcao['xy'])
                    tamanho_texto_cidade_uf = tuple(opcao['size_text'])
        else:
            xy_cidade_uf_empresa = tuple(self.opcoes['XY_CIDADE_UF_EMPRESA'])

        try:
            img = Image.open("image/{}.jpg".format(self.certificado.ano))

            texto_empresa_png = self.escreve_img(
                texto_img=str(self.certificado.nome_fantasia).rstrip() + ' ').resize(tamanho_texto_empresa)

            texto_segmento_empresa_png = self.escreve_img(
                texto_img=str(self.certificado.segmento).rstrip() + ' ').resize(tamanho_texto_segmento)

            texto_cidade_uf_empresa_png = self.escreve_img(texto_img=str(
                self.certificado.cidade + '-' + self.certificado.uf).rstrip()).resize(
                tamanho_texto_cidade_uf)

            img.paste(texto_empresa_png, tuple(self.opcoes['XY_NOME_EMPRESA']),
                      texto_empresa_png)

            img.paste(texto_segmento_empresa_png, tuple(self.opcoes['XY_SEGMENTO_EMPRESA']),
                      texto_segmento_empresa_png)

            img.paste(texto_cidade_uf_empresa_png, xy_cidade_uf_empresa, texto_cidade_uf_empresa_png)

            if modo_bot:
                return img
            else:
                if self.certificado.ano == '2024':
                    resized_img = img.resize((3505, 2449), Image.Resampling.LANCZOS)
                    resized_img.save("./certs/obj-{}{}.jpg".format(self.certificado.nome_fantasia, random.random()))
                    return

                return img.save("./certs/obj-{}{}.jpg".format(self.certificado.nome_fantasia, random.random()))

        except Exception as e:
            print(e)
