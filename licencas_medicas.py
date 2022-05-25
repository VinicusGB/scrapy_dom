from datetime import date, timedelta
from lib2to3.pytree import convert
import base
import os

dt_now = base.get_date_today()



BASE_DIR = 'C:\\Projetos\\scrapy_dom'
os.chdir(BASE_DIR)
try:
    os.makedirs(f'{BASE_DIR}\\outputs_files\\{dt_now}')
    print(f'### MAKEDIRS CONCLUÍDO - Verifique a pasta: {BASE_DIR}\\outputs_files\\{dt_now}')
except:
    print(f'### MAKEDIRS PASTA EXISTENTE - Verifique a pasta: {BASE_DIR}\\outputs_files\\{dt_now}')
    pass

DATA_DIR = BASE_DIR + '\\querido-diario\\data_collection\\data\\3550308\\'+ dt_now
SAVE_DIR = BASE_DIR + '\\outputs_files\\' + dt_now
DATA_FILE = [f for f in os.listdir(SAVE_DIR) if f.endswith("tsv")][0]
os.chdir(DATA_DIR)

print(f'BASE_DIR:  {BASE_DIR}')
print(f'DATA_DIR:  {DATA_DIR}')
print(f'SAVE_DIR:  {SAVE_DIR}')
print(f'DATA_FILE: {DATA_FILE}')
print(f'DOM-SP:    {dt_now}')


with open(SAVE_DIR + '\\' + DATA_FILE,'r') as file:
    conteudo = file.read()

sc_servidores = conteudo.find('\nSERVIDORES\n')
sc_concursos = conteudo.find('\nCONCURSOS\n')

conteudo_servidores = conteudo[sc_servidores:sc_concursos].replace('\t','')

sc_licencas_medicas = conteudo_servidores.find('\nRELAÇÃO DE LICENÇA MÉDICA\n')
sc_lm_8989 = conteudo_servidores.find('\nRelação de Licenças Médicas nos Termos da Lei 8989/79')
sc_lm_8989_negada = conteudo_servidores.find('\nRelação de Licenças Médicas Negadas nos Termos da Lei')
sc_lm_fim = conteudo_servidores.find('\nDIVISÃO DE PERÍCIA MÉDICA - COGESS\nSEÇÃO DE LICENÇAS MÉDICAS\nRELAÇÃO DE FALTA DO SERVIDOR À PERÍCIA\n')
sc_lm_retificadas = conteudo_servidores.find('\nRELAÇÃO DE LICENÇAS MÉDICAS RETIFICADAS EM FUN-\n')
sc_obito_servidor = conteudo_servidores.find('ÓBITO DO SERVIDOR\n')

lm_8989 = conteudo_servidores[sc_lm_8989:sc_lm_8989_negada]
lm_8989_2 = conteudo_servidores[sc_lm_8989:sc_lm_8989_negada]
lm_8989_negada = conteudo_servidores[sc_lm_8989_negada:sc_lm_fim]
lm_retificadas = conteudo_servidores[sc_lm_retificadas:sc_obito_servidor]
