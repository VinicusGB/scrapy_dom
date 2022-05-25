from datetime import date, timedelta
from lib2to3.pytree import convert
import base
import os

BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES = base.get_directories()


with open(DATA_FILE,'r') as file:
    conteudo = file.read()

sc_servidores = conteudo.find('\nSERVIDORES\n')
sc_concursos = conteudo.find('\nCONCURSOS\n')

conteudo_servidores = conteudo[sc_servidores:sc_concursos]
base.save_csv(SAVE_DIR,conteudo_servidores,'servidores')

sc_licencas_medicas = conteudo_servidores.find('\nRELAÇÃO DE LICENÇA MÉDICA')
sc_lm_8989 = conteudo_servidores.find('\nRelação de Licenças Médicas nos Termos da Lei 8989/79')
sc_lm_8989_negada = conteudo_servidores.find('\nRelação de Licenças Médicas Negadas nos Termos da Lei')
sc_lm_fim = conteudo_servidores.replace('\t','').find('\nDIVISÃO DE PERÍCIA MÉDICA - COGESS')
sc_lm_retificadas = conteudo_servidores.find('\nRELAÇÃO DE LICENÇAS MÉDICAS RETIFICADAS EM FUN-\n')
sc_obito_servidor = conteudo_servidores.find('ÓBITO DO SERVIDOR\n')

lm_8989 = conteudo_servidores[sc_lm_8989:sc_lm_8989_negada]
base.save_csv(SAVE_DIR,lm_8989,'licenca_8989')
lm_8989_2 = conteudo_servidores[sc_lm_8989:sc_lm_8989_negada]
lm_8989_negada = conteudo_servidores[sc_lm_8989_negada:sc_lm_fim]
lm_retificadas = conteudo_servidores[sc_lm_retificadas:sc_obito_servidor]
