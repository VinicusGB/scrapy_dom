import subprocess
from datetime import datetime

from scripts.remoto.functions import foi_baixado, foi_tratado

class Remoto():
    '''Classe do diretório remoto'''
    def __init__(self, published = datetime.now().date()):
        subprocess.os.chdir('c:\Projetos\scrapy_dom')
        self.published = published
        self.base = subprocess.os.path.join(subprocess.os.getcwd(),'querido-diario','data_collection')
        self.dir = subprocess.os.path.join(self.base,'data','3550308',str(published))
        self.baixado, self.arquivos_baixados = foi_baixado(self)
        self.tratado = foi_tratado(self)
    def baixar(self):
        subprocess.os.chdir('c:\Projetos\scrapy_dom')
        try:
            [subprocess.os.remove(subprocess.os.path.join(self.dir,arquivo)) for arquivo in self.arquivos_baixados]
            subprocess.os.removedirs(self.dir)
            print("Arquivos apagados")
        except FileNotFoundError:
            print("Diretório não existe")
            pass   
        subprocess.os.chdir(self.base)
        print("Baixando o diário")
        subprocess.call(["scrapy","crawl","sp_sao_paulo","-a",f"start_date={str(self.published)}"])
        print("Diário baixado")
