class Certificado:

    def __init__(
            self, nome_fantasia='', nome_divulgacao='', segmento='', cidade='', uf='',
            telefone='', preco='', obs='', tipo='', retroativos=None, ano='2023'
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
        self.ano = ano
