'''
Funções principais utilizadas na class remoto
'''

import subprocess
from functools import reduce

def foi_baixado(self):
    '''Método que verfica se os arquivos foram baixados, tratados e lista os arquivos'''
    try: return True, subprocess.os.listdir(self.dir.remoto)
    except: return False, []

def foi_tratado(self):
    '''Método para verificar se os arquivos foram tratados'''
    if self.baixado == True: return bool(reduce(lambda a,b: (str(a).startswith('pg_',0,3)) + (str(b).startswith('pg_',0,3)), self.arquivos_baixados))
    else: return False

def baixar(self):
    subprocess.os.chdir(self.dir.base)
    try:
        [subprocess.os.remove(subprocess.os.path.join(self.dir,arquivo)) for arquivo in self.arquivos_baixados]
        subprocess.os.removedirs(self.dir)
        print("Arquivos apagados")
    except FileNotFoundError:
        print("Diretório não existe")
        pass 
