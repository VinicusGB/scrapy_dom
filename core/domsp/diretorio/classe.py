import subprocess
from datetime import datetime

from scripts.diretorio.functions import baixado, tratado

class Diretorio():
    '''Classe dos diretórios para salvar os dados'''
    def __init__(self, published = datetime.today().date()):
        self.base = subprocess.os.getcwd()
        self.remoto = subprocess.os.path.join(self.base,'querido-diario','data_collection','data','3550308',str(published))
        self.local = subprocess.os.path.join(self.base,'outputs_files',str(published))
        self.baixado = baixado(self)
        self.tratado = tratado(self)
    def __str__(self):
        return self.base
