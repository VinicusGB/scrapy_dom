import subprocess
from datetime import datetime

from scripts.local.functions import foi_baixado, foi_tratado

class Local():
    '''Classe do diretório local'''
    def __init__(self, published = datetime.now().date()):
        self.published = published
        self.base = subprocess.os.path.join(subprocess.os.getcwd())
        self.dir = subprocess.os.path.join(self.base,'outputs_files',str(published))
        self.baixado, self.arquivos_baixados = foi_baixado(self)
        self.tratado = foi_tratado(self)

del subprocess
del datetime
