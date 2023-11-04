import subprocess
from datetime import datetime, date

from core.domsp.functions import houve_publicacao, obter_informacao_dom, foi_baixado, baixar, foi_tratado, tratar_remoto, remoto_merge_local, local_convert_tsv, local_limpa_dados
from core.domsp.diretorio.classe import Diretorio

class DOMSP():
    '''Classe do Diário Oficial do Município de São Paulo - (DOM SP)'''
    def __init__(self, published = datetime.now().date(), varbaixar  = True, vartratar = True, varacompanhar = False):
        '''Método que instância o objeto do DOM SP'''
        #subprocess.os.chdir('c:\Projetos\scrapy_dom')
        print(f"\n### SCRAPY-DOM ###")
        self.published = houve_publicacao(published)
        print(f"Data de publicação: {self.published}\n")
        self.dir = Diretorio(self.published)
        self.baixado, self.arquivos_baixados = foi_baixado(self)
        self.tratado = foi_tratado(self)
        self.varbaixar = varbaixar
        self.vartratar = vartratar
        self.varacompanhar = varacompanhar
        self.year, self.edition, self.pags, self.head, self.dom = obter_informacao_dom(self)
    def __str__(self):
        '''Método para quando o objeto e chamado'''
        return print(f"\
        \n### Diário Oficial do Município de São Paulo ###\n\
        Data de publicação: {self.published}\
        ")
    def foi_baixado(self):
        self.baixado, self.arquivos_baixados = foi_baixado(self)
    def baixar(self):
        baixar(self)
    def obter_informacao_dom(self):
        self.year, self.edition, self.pags, self.head, self.dom = obter_informacao_dom(self)
    def renomear_arquivos_baixados(self):
        tratar_remoto(self)
    def juntar_arquivos_baixados(self):
        remoto_merge_local(self)
    def converter_arquivos_baixados_tsv(self):
        local_convert_tsv(self)
    def limpar_dados(self):
        local_limpa_dados(self)