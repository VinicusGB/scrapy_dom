'''
Funções principais utilizadas na class local
'''

import subprocess

def foi_baixado(self):
    '''Método que verfica se os arquivos foram baixados, tratados e lista os arquivos'''
    try: return True, subprocess.os.listdir(self.dir)
    except: return False, []
def foi_tratado(self):
    '''Método para verificar se os arquivos foram tratados'''
    if self.baixado == True: return bool(reduce(lambda a,b: (str(a).startswith('pg_',0,3)) + (str(b).startswith('pg_',0,3)), self.arquivos_baixados))
    else: return False

del subprocess
