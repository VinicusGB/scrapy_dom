'''
Funções principais utilizadas na class diretorio
'''

import subprocess

def baixado(self):
    '''
    Verifica se o diretório remoto(querido-diario/data_collection/) foi baixado e retorna True/False
    '''
    try: return True, subprocess.os.listdir(self.remoto)
    except: return False, []
def tratado(self):
    '''
    Verifica se o diretório local(outputs_files/) foi baixado e retorna True/False
    '''
    try: return True, subprocess.os.listdir(self.local)
    except: return False, []


del subprocess