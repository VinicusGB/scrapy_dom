import subprocess
from datetime import datetime

from scripts.domsp.functions import houve_publicacao
from scripts.diretorio.classe import Diretorio
from scripts.local.classe import Local
from scripts.remoto.classe import Remoto

class DOMSP():
    '''Classe do Diário Oficial do Município de São Paulo - (DOM SP)'''
    def __init__(self, published = datetime.now().date()):
        '''Método que instância o objeto do DOM SP'''
        subprocess.os.chdir('c:\Projetos\scrapy_dom')
        print(f"Diário Oficial do Município de São Paulo")
        self.published = houve_publicacao(published)
        print(f"Data de publicação: {self.published}")
        self.year = published.year - 1955
        self.dir = Diretorio(self.published)
        self.remoto = Remoto(self.published)
        self.local = Local(self.published)
        self.edition = 0
        self.pags = 0
        self.head = f'São Paulo, {str(self.year)} ({str(self.edition)})'
    def __str__(self):
        '''Método para quando o objeto e chamado'''
        return print(f"\
        Diário Oficial do Município de São Paulo\n\
        Data de publicação: {self.published}\
        ")
