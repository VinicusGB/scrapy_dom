import subprocess
from datetime import datetime

from core.domsp.remoto.functions import foi_baixado

class Diretorio():
    '''Classe dos diretórios para salvar os dados'''
    def __init__(self, published = datetime.today().date()):
        self.base = subprocess.os.getcwd()
        self.local = subprocess.os.path.join(self.base,'outputs',str(published))
        self.dom_despachos, self.dom_servidores, self.dom_concursos, self.dom_editais, self.dom_licitacoes, self.dom_camara, self.dom_tribunal, self.dom = [subprocess.os.path.join(self.local,diretorio) for diretorio in ['DESPACHOS','SERVIDORES','CONCURSOS','EDITAIS','LICITAÇÕES','CÂMARA MUNICIPAL','TRIBUNAL DE CONTAS','00-DOM COMPLETO']]
        self.remoto = subprocess.os.path.join(self.base,'core','querido-diario','data_collection','data','3550308',str(published))
        self.querido_diario = subprocess.os.path.join(self.base,'core','querido-diario','data_collection')
        self.baixado, self.arquivos_baixados = foi_baixado(self)
        self.makedirs()
    def __str__(self):
        return self.base
    def makedirs(self):
        try:
            [subprocess.os.makedirs(subprocess.os.path.join(self.local,diretorio)) for diretorio in ['','DESPACHOS','SERVIDORES','CONCURSOS','EDITAIS','LICITAÇÕES','CÂMARA MUNICIPAL','TRIBUNAL DE CONTAS','00-DOM COMPLETO']]
        except IOError as erro:
            print(f"### DIRETÓRIOS: {erro} ###")
