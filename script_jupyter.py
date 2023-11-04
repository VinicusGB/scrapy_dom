# %% [markdown]
# # Script para ler o Diário Oficial do Município de São Paulo

# %% [markdown]
# ## Script BASE
# http://diariooficial.imprensaoficial.com.br/doflash/prototipo/2022/julho/19/cidade/pdf/pg_0005.pdf

# %% [markdown]
# ### Importando as bibliotecas

# %%
from datetime import date, datetime, timedelta
from PyPDF2 import PdfFileReader, PdfFileMerger
from collections import OrderedDict
import os
import subprocess
import fitz as fz
import tabula
import pandas as pd
import scripts
import random
import re

# %%
BASE_DIR = os.getcwd()
BASE_DIR

# %%
SCRAPY_DIR = os.path.join(BASE_DIR,'core','querido-diario','data_collection')
SCRAPY_DIR

# %%
#SCRAPY_DIR = f'{BASE_DIR}\\querido-diario\\data_collection'
os.chdir(SCRAPY_DIR)
os.getcwd()

# %% [markdown]
# ### Obter data atual

# %%
def get_date_today():
    '''Obtém a data atual e retorna uma string: (YYYY-mm-dd)'''
    dt_now = date.today()
    if dt_now.weekday() == 0:
            dt_now = dt_now + timedelta(-2)
            dt_now = dt_now.strftime("%Y-%m-%d")
    else:
            dt_now = dt_now.strftime("%Y-%m-%d")
    dt_now = '2023-01-24'
    return dt_now

dt_now = get_date_today()
print(dt_now)


# %%
!scrapy crawl sp_sao_paulo -a start_date={dt_now}

# %% [markdown]
# ### Criando o diretório SAVE_DIR

# %%
BASE_DIR

# %%
#BASE_DIR = os.getcwd()
os.chdir(BASE_DIR)
try:
    os.makedirs(os.path.join(BASE_DIR,'outputs',dt_now))
    SAVE_DIR = os.path.join(BASE_DIR,'outputs',dt_now)
    print(f"### MAKEDIRS CONCLUÍDO - Verifique a pasta: {SAVE_DIR}")
except IOError as erro:
    print(f"### MAKEDIRS PASTA EXISTENTE - Verifique a pasta: {erro}")
    pass

# %% [markdown]
# ### Obter diretórios

# %%
def get_directories():
        '''Obtém  os diretórios de trabalho.
                return BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES
        '''
        dt_now = get_date_today()
        #BASE_DIR = f'c:\\Projetos\\scrapy_dom'
        os.chdir(BASE_DIR)
        try:
                os.makedirs(os.path.join(BASE_DIR,'outputs',dt_now))
        except:
                pass

        #DATA_DIR = f'{BASE_DIR}\\querido-diario\\data_collection\\data\\3550308\\{str(dt_now)}'
        DATA_DIR = os.path.join(BASE_DIR,'core','querido-diario','data_collection','data','3550308',dt_now)
        #SAVE_DIR = f'{BASE_DIR}\\outputs_files\\{dt_now}'
        SAVE_DIR = os.path.join(BASE_DIR,'outputs',dt_now)
        # DATA_FILE = SAVE_DIR + '\\' + [f for f in os.listdir(SAVE_DIR) if f.endswith("tsv")][0]
        DATA_FILES = os.listdir(DATA_DIR)
        DATA_FILES.sort()
        
        print(f'###   INFO:  DIRS   ###')
        print(f'  BASE_DIR:  {BASE_DIR}')
        print(f'  DATA_DIR:  {DATA_DIR}')
        print(f'  SAVE_DIR:  {SAVE_DIR}')
        #print(f' DATA_FILE:  {DATA_FILE}')
        #print(f'DATA_FILES:  {DATA_FILES}')
        
        return BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILES

BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILES = get_directories()

# %% [markdown]
# ### Obtendo Informações do DOM

# %%
def get_info_dom():
        '''Obtém as informações do DOM.
                return YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM        
        '''
        dt_now = get_date_today()
        BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILES = get_directories()
        PAGS_DOM = str(len(DATA_FILES))
        
        with fz.open(os.path.join(DATA_DIR,DATA_FILES[random.randint(0,int(PAGS_DOM)-1)])) as file:
                print(file)
                search_edition = ''
                for page in file:
                        search_edition += page.get_text()

        #CABECALHO_DOM = re.compile(r'(.(\d+) \W )?(São Paulo, (\d+) \((\d+)\))( \W (\d+).)?')
        #CABECALHO_DOM = re.compile(r'(São Paulo,.?(\d+).?\((\d+)\))',re.DOTALL)
        CABECALHO_DOM = re.compile(r'((\d+) \W )?(São Paulo, (\d+) \((\d+)\))( \W (\d+))?')
        #CABECALHO_DOM = r'.?[0-9]{0,3}.?[–]?.?São Paulo,.?[0-9]{1,3}.?\([0-9]{1,3}\).?[–]?.?[0-9]{0,3}'gima
        print(f"TESTE ANTES:\n{CABECALHO_DOM.search(search_edition).group()}")
        #YEAR_DOM = date.today().year - 1955
        HEAD_DOM = CABECALHO_DOM.search(search_edition).group(3)
        YEAR_DOM = CABECALHO_DOM.search(search_edition).group(4)
        EDITION_DOM = CABECALHO_DOM.search(search_edition).group(5)
        PAG_EVEN_DOM = CABECALHO_DOM.search(search_edition).group(2)
        PAG_ODD_DOM = CABECALHO_DOM.search(search_edition).group(7)
        PAG_DOM = (str(PAG_EVEN_DOM) + str(PAG_ODD_DOM)).replace('None','')
        #HEAD_DOM ='São Paulo, ' + str(YEAR_DOM) + ' ('
        
        #search_edition = search_edition[search_edition.find(HEAD_DOM):]
        #EDITION_DOM = search_edition[search_edition.find('(')+1:search_edition.find(')')]
        #HEAD_DOM ='São Paulo, ' + str(YEAR_DOM) + ' (' + EDITION_DOM + ')'
        #HEAD_DOM = 'São Paulo, 67 (131)'
        PAGS_DOM = str(len(DATA_FILES))
        DOM = f'DOM_SP-{str(YEAR_DOM)}_{str(EDITION_DOM)}_{PAGS_DOM}_{str(dt_now)}'
        #DOM = 

        print(f"TESTE DEPOIS:\n{type(PAG_DOM)} {PAG_DOM}")
        print('### INFO: DOM-SP ###')
        print(f'DATA: {dt_now}')
        print(f'PAGS: {PAGS_DOM}')
        print(f'HEAD: {HEAD_DOM}')
        print(f' DOM: {DOM}')
        
        return YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM,DOM

YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM,DOM = get_info_dom()

# %% [markdown]
# ### Renomeando arquivos

# %%
contexts = ''
for file_name in DATA_FILES:
        print('Obtendo conteúdo de: ' + file_name)
        with fz.open(os.path.join(DATA_DIR,file_name)) as file:
                context = ""
                for page in file:
                        context += '<pag>\n'+ page.get_text() + '</pag>\n'
                
                odd_page = "São Paulo, " + str(YEAR_DOM) + " (" + str(EDITION_DOM) + ") – "
                even_page = " – São Paulo, " + str(YEAR_DOM) + " (" + str(EDITION_DOM) + ")"

                if  context.find(odd_page) != -1:
                        num_page = context[context.find(odd_page)+len(odd_page):context.find('\n',context.find(odd_page))]
                elif context.find(even_page) != -1:
                        num_page = context[context.find('\n',context.find(even_page)-5)+1:context.find(even_page)]
                elif context.find("D.O.C.; " + HEAD_DOM) != -1:
                        num_page = str(len(DATA_FILES))
                elif context.find("Ano "+ str(YEAR_DOM)) != -1:
                        num_page = '1'
                else:
                        num_page = ''

        contexts += context
        os.rename(os.path.join(DATA_DIR,file_name),os.path.join(DATA_DIR,f'pg_{(num_page.strip()).zfill(3)}-{file_name}'))

DATA_FILES = os.listdir(DATA_DIR)
DATA_FILES.sort()
print(f'### RENAME CONCLUÍDO - Verifique a pasta: {DATA_DIR} ###')

# %%
ARQUVIOS = os.listdir(DATA_DIR)
ARQUVIOS.sort()
ARQUVIOS

# %% [markdown]
# ### Juntando os arquivos

# %%
SAVE_DIR

# %%
pdf_files = [f for f in ARQUVIOS if f.endswith("pdf")]
merger = PdfFileMerger()

for filename in pdf_files:
    print(f'Merge de: {filename}')
    merger.append(PdfFileReader(os.path.join(DATA_DIR, filename), "rb"))

merger.write(os.path.join(SAVE_DIR ,f"DOM_SP-{str(YEAR_DOM)}_{str(EDITION_DOM)}_{str(len(DATA_FILES))}_{str(dt_now)}.pdf"))
print(f'### MERGE CONCLUÍDO - Verifique a pasta: {SAVE_DIR} ###')

# %% [markdown]
# ### Convertendo para TSV FINAL

# %%
SAVE_DIR

# %%
try:
    print('Convertendo arquivo para TSV')
    area_text = [[42.849,28.172,1209.134,215.329],[42.849,216.314,1210.119,393.621],[42.849,395.591,1210.119,574.868],[42.849,576.838,1207.164,760.055]]
    #tabula.convert_into_by_batch(SAVE_DIR,output_format="tsv",area=area_text,pages="all")
    tabula.convert_into_by_batch(SAVE_DIR,output_format="tsv",area=area_text,pages="all")
    print(f'### CONVERT CONCLUÍDO - Verifique a pasta: {SAVE_DIR} ###')
except EOFError as erro:
    print(f'### CONVERT CONCLUÍDO COM EXCEÇÃO - Verifique a pasta: {SAVE_DIR}\n{erro} ###')

# %%
def get_directories():
        '''Obtém  os diretórios de trabalho.
                return BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES
        '''
        dt_now = get_date_today()
        BASE_DIR = os.getcwd()
        os.chdir(BASE_DIR)
        try:
                os.makedirs(os.path.join(BASE_DIR,'outputs',dt_now))
        except:
                pass

        DATA_DIR = os.path.join(BASE_DIR,'core','querido-diario','data_collection','data','3550308',str(dt_now))
        SAVE_DIR = os.path.join(BASE_DIR,'outputs',dt_now)
        DATA_FILE = os.path.join(SAVE_DIR,[f for f in os.listdir(SAVE_DIR) if f.endswith("tsv")][0])
        DATA_FILES = os.listdir(DATA_DIR)
        DATA_FILES.sort()
        
        print(f'###   INFO:  DIRS   ###')
        print(f'  BASE_DIR:  {BASE_DIR}')
        print(f'  DATA_DIR:  {DATA_DIR}')
        print(f'  SAVE_DIR:  {SAVE_DIR}')
        print(f' DATA_FILE:  {DATA_FILE}')
        print(f'DATA_FILES:  {DATA_FILES}')
        
        return BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES

BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES = get_directories()

# %% [markdown]
# ### Salva arquivo final

# %%
def save_file(SAVE_DIR,CONTEXT,NAME_FILE,FORMAT='txt'):
        '''
                Cria um arquivo com o conteúdo e salva na pasta.
                        SAVE_DIR  : Diretório para salvar o conteúdo
                        CONTEXT   : Conteúdo a ser salvo
                        NAME_FILE : Nome do arquivo para ser salvo
                        FORMAT    : Formato do arquivo final
        '''

        with open(f"{SAVE_DIR}\\{NAME_FILE}.{FORMAT}","w",encoding='utf-8') as output_file:
                output_file.write(CONTEXT)
        
        return f"{SAVE_DIR}\\{NAME_FILE}.{FORMAT}"

# %%
def add_file(SAVE_DIR,CONTEXT,NAME_FILE,FORMAT='txt'):
        '''
                Cria um arquivo com o conteúdo e salva na pasta.
                        SAVE_DIR  : Diretório para salvar o conteúdo
                        CONTEXT   : Conteúdo a ser salvo
                        NAME_FILE : Nome do arquivo para ser salvo
                        FORMAT    : Formato do arquivo final
        '''
        print(NAME_FILE)
        with open(f"{SAVE_DIR}\\{NAME_FILE}.{FORMAT}","a",encoding='utf-8') as output_file:
                output_file.write(CONTEXT)
        return f"{SAVE_DIR}\\{NAME_FILE}.{FORMAT}"

# %% [markdown]
# ### Definindo Diretórios

# %% [markdown]
# 
# ### Obtem contéudo do arquivo TSV

# %%
with open(DATA_FILE,'r') as file:
    conteudo = file.read()

# %% [markdown]
# ## Scripts de Listagens

# %% [markdown]
# ### Limpeza dos dados

# %%
def limpa_tabulacao(conteudo):
    conteudo = conteudo.replace('-\n','')
    conteudo = conteudo.replace(',\n',', ')
    conteudo = conteudo.replace('\npara ',' para ')
    conteudo = conteudo.replace('\nna ',' na ')
    conteudo = conteudo.replace('\nno ',' no ')
    conteudo = conteudo.replace('\nda ',' da ')
    conteudo = conteudo.replace(' da\n',' da ')
    conteudo = conteudo.replace('\nde ',' de ')
    conteudo = conteudo.replace(' de\n',' de ')
    conteudo = conteudo.replace('\ndo ',' do ')
    conteudo = conteudo.replace(' do\n',' do ')
    return conteudo

# %%
limpa_preposicao_daeos = re.compile(' [dD][aeoAEO]\n')

# %% [markdown]
# ### Seções / Cadernos

# %%
conteudo_dom = conteudo

# %%
sc_servidores = re.compile(r'\nSERVIDORES\n')
sc_servidores.finditer(conteudo_dom)


# %%
sc_concursos = re.compile(r'\nCONCURSOS\n')
sc_concursos.finditer(conteudo_dom)

# %%
sc_editais = re.compile(r'\nEDITAIS\n')
sc_editais.finditer(conteudo_dom)

# %%
sc_licitacoes = re.compile(r'\nLICITAÇÕES\n')
lc_licitacoes = sc_licitacoes.finditer(conteudo_dom)
print(type(lc_licitacoes))
for lc in lc_licitacoes:
    print(type(lc.start()))
    print(conteudo_dom[lc.start()-20:lc.end()+20])
    print(lc.start())

# %%
sc_camara_municipal = re.compile(r'\nCÂMARA MUNICIPAL\n')
sc_camara_municipal.finditer(conteudo_dom)

# %%
sc_tribunal_de_contas = re.compile(r'\nTRIBUNAL DE CONTAS\n')
sc_tribunal_de_contas.finditer(conteudo_dom)

# %%
note_secretarias = conteudo.find('\nSECRETARIAS\n')
note_servidores = conteudo.find('\nSERVIDORES\n')
note_concursos = conteudo.find('\nCONCURSOS\n')


# %%
conteudo_secretarias = conteudo[note_secretarias:note_servidores]
conteudo_servidores = conteudo[note_servidores:note_concursos]

# %%
conteudo_secretarias = limpa_tabulacao(conteudo_secretarias)
#conteudo_secretarias

# %% [markdown]
# ### Seção SERVIDORES

# %%
conteudo_alterado = conteudo

# %% [markdown]
# #### Limpeza dos dados

# %%
def limpa_tabulacao(conteudo_alterado):
    print('### LIMPA TABULAÇÃO ###')
    print(f'Qtd de linhas antes: {len(conteudo_alterado)}')
    qtd_len_inicial = len(conteudo_alterado)
    qtd_len_final = 0
    while qtd_len_final < qtd_len_inicial:
        qtd_len_inicial = len(conteudo_alterado)
        conteudo_alterado = conteudo_alterado.replace('\t',' ')
        conteudo_alterado = conteudo_alterado.replace('""','')
        conteudo_alterado = conteudo_alterado.replace('\n\n\n','\n')
        conteudo_alterado = conteudo_alterado.replace('\n\n','\n')
        conteudo_alterado = conteudo_alterado.replace(' \n','\n')
        conteudo_alterado = conteudo_alterado.replace('\n ','\n')
        conteudo_alterado = conteudo_alterado.replace('    ',' ')
        conteudo_alterado = conteudo_alterado.replace('   ',' ')
        conteudo_alterado = conteudo_alterado.replace('  ',' ')
        conteudo_alterado = conteudo_alterado.replace('-\n','')
        conteudo_alterado = conteudo_alterado.replace('\n- ',' - ')
        conteudo_alterado = conteudo_alterado.replace('\n– ',' – ')
        conteudo_alterado = conteudo_alterado.replace(',\n',', ')
        conteudo_alterado = conteudo_alterado.replace(', \n',', ')
        conteudo_alterado = conteudo_alterado.replace('\n, ',', ')
        conteudo_alterado = conteudo_alterado.replace('/\n','/')
        conteudo_alterado = conteudo_alterado.upper()
        qtd_len_final = len(conteudo_alterado)
    print(f'Qtd de linhas depois: {len(conteudo_alterado)}')
    return conteudo_alterado

# %%
def normaliza_cabecalho(conteudo_alterado):
    print('### NORMALIZA CABEÇALHO ###')
    print(f'Qtd de linhas antes: {len(conteudo_alterado)}')
    qtd_len_inicial = len(conteudo_alterado)
    qtd_len_final = 0
    while qtd_len_final < qtd_len_inicial:
        qtd_len_inicial = len(conteudo_alterado)
        conteudo_alterado = conteudo_alterado.replace('E.H.','EH')
        conteudo_alterado = conteudo_alterado.replace('E.H ','EH ')
        conteudo_alterado = conteudo_alterado.replace('REG. FUNC.','RF')
        conteudo_alterado = conteudo_alterado.replace('REG.FUNC.','RF')
        conteudo_alterado = conteudo_alterado.replace('REG. FUNC/','RF/VINCULO')
        conteudo_alterado = conteudo_alterado.replace('REG. FUNC/VINC ','RF/VINC ')
        conteudo_alterado = conteudo_alterado.replace('REG VINC ','RF VINCULO ')
        conteudo_alterado = conteudo_alterado.replace('RF./','RF/')
        conteudo_alterado = conteudo_alterado.replace('R.F.','RF')
        conteudo_alterado = conteudo_alterado.replace('RF. ','RF ')
        conteudo_alterado = conteudo_alterado.replace(' VINC.',' VINCULO')
        conteudo_alterado = conteudo_alterado.replace('RF/VINC ','RF/VINCULO ')
        conteudo_alterado = conteudo_alterado.replace('DURAÇÃO','DURACAO')
        conteudo_alterado = conteudo_alterado.replace('A PARTIR DE','A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('A PARTIR','A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace(' ART.','ARTIGO')
        conteudo_alterado = conteudo_alterado.replace('PERÍODO','PERIODO')
        conteudo_alterado = conteudo_alterado.replace(' VÍNC.',' VINCULO')
        conteudo_alterado = conteudo_alterado.replace(' QTE DE DIAS ',' DIAS ')
        conteudo_alterado = conteudo_alterado.replace(' NO DE DIAS ',' DIAS ')
        conteudo_alterado = conteudo_alterado.replace('RF/V ','RF/VINCULO ')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO FUNCIONAL NOME A_PARTIR_DE','RF NOME A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO FUNCIONAL NOME ','RF NOME ')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO NOME CARGO EXER- Q U A N - A_PARTIR_DE\nFUNCIONAL CÍCIO TIDADE','RF NOME CARGO EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO NOME CARGO EXER- QUAN- A_PARTIR_DE\nFUNCIONAL CÍCIO TIDADE','RF NOME CARGO EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO NOME CARGO EXER- QUANTI- A_PARTIR_DE\nFUNCIONAL CÍCIO DADE','RF NOME CARGO EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('EH R.F/V NOME QTE DE A_PARTIR_DE\nDIAS','EH RF NOME DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF NOME DIAS A PARTIR DE ARTIGO','RF NOME DIAS A_PARTIR_DE ARTIGO')
        conteudo_alterado = conteudo_alterado.replace('RF NOME A PARTIR DE','RF NOME A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF NOME DUR A_PARTIR_DE','RF NOME DURACAO A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF SERVIDOR CONTROLE NO','RF NOME CONTROLE_NO')
        conteudo_alterado = conteudo_alterado.replace('RF SERVIDOR DIAS A_PARTIR_DE','RF NOME DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF NOME CONTROLE NO','RF NOME CONTROLE_NO')
        conteudo_alterado = conteudo_alterado.replace('RF/V NOME DIAS/EXERCÍCIO A PARTIR DE','RF/VINCULO NOME DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF/VINCULO NOME DIAS A_PARTIR_DE','RF/VINCULO NOME DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF/VINCULO NOME NO DE DIAS A_PARTIR_DE PARENTESCO','RF/VINCULO NOME DIAS A_PARTIR_DE PARENTESCO')
        conteudo_alterado = conteudo_alterado.replace('RF/VINC NOME NÍVEL CAT. SÍMBOLO A PARTIR DE','RF/VINCULO NOME NIVEL_CAT SIMBOLO A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF NOME CARGO','RF NOME CARGO')
        conteudo_alterado = conteudo_alterado.replace('RF V NOME EH A PARTIR DE MOTIVO','RF VINCULO NOME EH A_PARTIR_DE MOTIVO')
        conteudo_alterado = conteudo_alterado.replace('R.F/V. NOME QTE DIAS A_PARTIR_DE','RF/VINCULO NOME DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF VINCULO NOME CARGO A PARTIR DE','RF VINCULO NOME CARGO A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('NOME RF DATA HORARIO','NOME RF DATA_HORARIO')
        conteudo_alterado = conteudo_alterado.replace('NOME RF DATAHORARIO','NOME RF DATA_HORARIO')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO VINC. NOME NIIVEL CAT.','RF VINCULO NOME NIIVEL CAT')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO VINC. NOME NIIVEL CAT. SIM','RF VINCULO NOME NIVEL CAT SIM')
        conteudo_alterado = conteudo_alterado.replace('RF VINC NOME NIIVEL CAT','RF VINCULO NOME NIVEL CAT')
        conteudo_alterado = conteudo_alterado.replace('REG. FUNC. NOME CARGO REGIME EXP. AC. NO','RF NOME CARGO REGIME EXP_AC_NO')
        conteudo_alterado = conteudo_alterado.replace('EH RF NOME DURAÇÃO A PARTIR ART','EH RF NOME DURACAO A_PARTIR_DE ARTIGO')
        conteudo_alterado = conteudo_alterado.replace('EH RF/V NOME DURA- A_PARTIR_DE\nÇÃO','EH RF/VINCULO NOME DURACAO A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('EH RF/VC. NOME DUR. A_PARTIR_DEARTIGO','EH RF/VINCULO NOME DURACAO A_PARTIR_DE ARTIGO')
        conteudo_alterado = conteudo_alterado.replace('REG.FUNC. NOME DE PARA','RF NOME DE PARA')
        conteudo_alterado = conteudo_alterado.replace('RF NOME NOTA INDIVIDUAL NOTA INSTITUCIONAL NOTA FINAL','RF NOME NOTA_INDIVIDUAL NOTA_INSTITUCIONAL NOTA_FINAL')
        conteudo_alterado = conteudo_alterado.replace('RF NOME DURAÇÃO À PARTIR DE','RF NOME DURACAO A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF NOME PERCENTUAL BASE DE CÁLCULO DATA','RF NOME PERCENTUAL BASE_DE_CALCULO DATA')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO NOME CARGO EXERCÍCIO QUAN- A PARTIR DE FUNCIONAL TIDADE','RF NOME CARGO EXERCICIO QUANTIDADE A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF VINCULO NOME: PERÍODO DE :','RF VINCULO NOME PERIODO_DE')
        conteudo_alterado = conteudo_alterado.replace('RF/V NOME CARGO N°DIAS','RF/VINCULO NOME CARGO DIAS')
        conteudo_alterado = conteudo_alterado.replace('NOME RF A PARTIR DE','NOME RF A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF/V NOME A PARTIR DE','RF/VINCULO NOME A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF: NOME: PROCESSO: E.H.:','RF NOME PROCESSO EH')
        conteudo_alterado = conteudo_alterado.replace('EH RF/V NOME DIAS A_PARTIR_DE\nDIAS','EH RF/VINCULO NOME DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF NOME E.H. A PARTIR','RF NOME E.H. A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF/V NOME DIAS A PARTIR DE','RF/VINCULO NOME DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF VINCULO NOME: PERIODO DE :','RF VINCULO NOME PERIODO')
        conteudo_alterado = conteudo_alterado.replace('RF NOME CONTROLE_NO ','RF NOME CONTROLE_NO\n')
        conteudo_alterado = conteudo_alterado.replace('RF VINCULO NOME CARGO A_PARTIR_DE ','RF VINCULO NOME CARGO A_PARTIR_DE\n')
        conteudo_alterado = conteudo_alterado.replace('RF/VÍNCULO NOME EXERCICIO NO DE DIAS A_PARTIR_DE','RF/VINCULO NOME EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF/V NOME DIAS EXERCÍCIO INICIO','RF/VINCULO NOME DIAS EXERCICIO INICIO')
        conteudo_alterado = conteudo_alterado.replace('RF NOME CARGO REGIME EXP_AC_NO ','RF NOME CARGO REGIME EXP_AC_NO\n')
        conteudo_alterado = conteudo_alterado.replace('RF NOME CARGO EXERCICIO QUANTIDADE A_PARTIR_DE','RF NOME CARGO EXERCICIO QUANTIDADE A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF NOME DE PARA ','RF NOME DE PARA\n')
        conteudo_alterado = conteudo_alterado.replace('RF NOME NOTA_INDIVIDUAL NOTA_INSTITUCIONAL NOTA_FINAL ','RF NOME NOTA_INDIVIDUAL NOTA_INSTITUCIONAL NOTA_FINAL\n')
        conteudo_alterado = conteudo_alterado.replace('RF NOME DURACAO A_PARTIR_DE ','RF NOME DURACAO A_PARTIR_DE\n')
        conteudo_alterado = conteudo_alterado.replace('RF NOME PERCENTUAL BASE_DE_CALCULO DATA ','RF NOME PERCENTUAL BASE_DE_CALCULO DATA\n')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO NOME CARGO EXERCÍCIO QUAN- A PARTIR DE FUNCIONAL TIDADE','RF NOME CARGO EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('NOME RF A_PARTIR_DE ','NOME RF A_PARTIR_DE\n')
        conteudo_alterado = conteudo_alterado.replace('RF/V NOME A_PARTIR_DE ','RF/V NOME A_PARTIR_DE\n')
        conteudo_alterado = conteudo_alterado.replace('RF NOME A_PARTIR_DE ','RF NOME A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO NOME CARGO EXERCÍCIO QUANTIDADE A_PARTIR_DE FUNCIONAL','RF NOME CARGO EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO NOME CARGO EXERCÍ- QUANTI- A_PARTIR_DE\nFUNCIONAL CIO DADE','RF NOME CARGO EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('REGISTRO FUNCIONAL NOME CARGO E X E R C Í - QUANTI- A_PARTIR_DE\nCIO DADE','RF NOME CARGO EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('R E G I S T R O NOME CARGO EXER- QUANTI- A_PARTIR_DE\nFUNCIONAL CÍCIO DADE','RF NOME CARGO EXERCICIO DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('R. F. NOME DIA INICIO EXERC.','RF/VINCULO NOME DIA INICIO EXERCICIO')
        #conteudo_alterado = conteudo_alterado.replace('RF/VINCULO NOME DIAS A_PARTIR_DE','RF/VINCULO NOME DIAS A_PARTIR_DE\n')
        conteudo_alterado = conteudo_alterado.replace('R.F/V. NOME QTE. DIAS A_PARTIR_DE','RF/VINCULO NOME DIAS A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('RF/VINCULO NOME DIAS A_PARTIR_DE\nPARENTESCO','RF/VINCULO NOME DIAS A_PARTIR_DE PARENTESCO')
        conteudo_alterado = conteudo_alterado.replace('RF/VINCULO NOME NÍVEL CAT. SÍMBOLO A_PARTIR_DE\nVINC','RF/VINCULO NOME NIVEL CATEGORIA SIMBOLO A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace(' R.F/V ',' RF/VINCULO ')
        qtd_len_final = len(conteudo_alterado)
    print(f'Qtd de linhas depois: {len(conteudo_alterado)}')
    return conteudo_alterado

# %%
def limpa_conjuncao_preposicao(conteudo_alterado):
    print('### LIMPA CONJUNÇÃO E PREPOSIÇÃO ###')
    print(f'Qtd de linhas antes: {len(conteudo_alterado)}')
    qtd_len_inicial = len(conteudo_alterado)
    qtd_len_final = 0
    while qtd_len_final < qtd_len_inicial:
        qtd_len_inicial = len(conteudo_alterado)
        conteudo_alterado = conteudo_alterado.replace(' AO\n',' AO ')
        conteudo_alterado = conteudo_alterado.replace('\nAO ',' AO ')
        conteudo_alterado = conteudo_alterado.replace(' AOS\n',' AOS ')
        conteudo_alterado = conteudo_alterado.replace('\nAOS ',' AOS ')
        conteudo_alterado = conteudo_alterado.replace(' SÃO\n',' SÃO ')
        conteudo_alterado = conteudo_alterado.replace(' À\n',' À ')
        conteudo_alterado = conteudo_alterado.replace('\nÀ ',' À ')
        conteudo_alterado = conteudo_alterado.replace(' ÀS\n',' ÀS ')
        conteudo_alterado = conteudo_alterado.replace('\nÀS ',' ÀS ')
        conteudo_alterado = conteudo_alterado.replace(' AS\n',' AS ')
        conteudo_alterado = conteudo_alterado.replace('\nAS ',' AS ')
        conteudo_alterado = conteudo_alterado.replace(' E\n',' E ')
        conteudo_alterado = conteudo_alterado.replace(' O\n',' O ')
        conteudo_alterado = conteudo_alterado.replace(' OS\n',' OS ')
        conteudo_alterado = conteudo_alterado.replace('\nOS ',' OS ')
        conteudo_alterado = conteudo_alterado.replace(' OU\n',' OU ')
        conteudo_alterado = conteudo_alterado.replace('\nOU ',' OU ')
        conteudo_alterado = conteudo_alterado.replace(' DA\n',' DA ')
        conteudo_alterado = conteudo_alterado.replace('\nDA ',' DA ')
        conteudo_alterado = conteudo_alterado.replace(' DAS\n',' DAS ')
        conteudo_alterado = conteudo_alterado.replace('\nDAS ',' DAS ')
        conteudo_alterado = conteudo_alterado.replace(' DA(S)\n',' DA(S) ')
        conteudo_alterado = conteudo_alterado.replace('\nDA(S) ',' DA(S) ')
        conteudo_alterado = conteudo_alterado.replace(' DE\n',' DE ')
        conteudo_alterado = conteudo_alterado.replace('\nDE ',' DE ')
        conteudo_alterado = conteudo_alterado.replace(' DO\n',' DO ')
        conteudo_alterado = conteudo_alterado.replace('\nDO ',' DO ')
        conteudo_alterado = conteudo_alterado.replace(' DOS\n',' DOS ')
        conteudo_alterado = conteudo_alterado.replace('\nDOS ',' DOS ')
        conteudo_alterado = conteudo_alterado.replace(' DO(S)\n',' DO(S) ')
        conteudo_alterado = conteudo_alterado.replace('\nDO(S) ',' DO(S) ')
        conteudo_alterado = conteudo_alterado.replace(' COM\n',' COM ')
        conteudo_alterado = conteudo_alterado.replace('\nCOM ',' COM ')
        conteudo_alterado = conteudo_alterado.replace(' EM\n',' EM ')
        conteudo_alterado = conteudo_alterado.replace('\nEM ',' EM ')
        conteudo_alterado = conteudo_alterado.replace(' PARA\n',' PARA ')
        conteudo_alterado = conteudo_alterado.replace('\nPARA ',' PARA ')
        conteudo_alterado = conteudo_alterado.replace('\nP/ ',' PARA ')
        conteudo_alterado = conteudo_alterado.replace(' POR\n',' POR ')
        conteudo_alterado = conteudo_alterado.replace('\nPOR ',' POR ')
        conteudo_alterado = conteudo_alterado.replace('\nSEM ',' SEM ')
        conteudo_alterado = conteudo_alterado.replace(' SEM\n',' SEM ')
        conteudo_alterado = conteudo_alterado.replace(' NA\n',' NA ')
        conteudo_alterado = conteudo_alterado.replace(' NAS\n',' NAS ')
        conteudo_alterado = conteudo_alterado.replace('\nNAS ',' NAS ')
        conteudo_alterado = conteudo_alterado.replace(' NO\n',' NO ')
        conteudo_alterado = conteudo_alterado.replace('\nNO ',' NO ')
        conteudo_alterado = conteudo_alterado.replace(' NOS\n',' NOS ')
        conteudo_alterado = conteudo_alterado.replace('\nNOS ',' NOS ')
        qtd_len_final = len(conteudo_alterado)
    print(f'Qtd de linhas depois: {len(conteudo_alterado)}')
    return conteudo_alterado

# %%
def palavras_especificas(conteudo_alterado):
    print('### LIMPA PALAVRAS ESPECIFICAS ###')
    print(f'Qtd de linhas antes: {len(conteudo_alterado)}')
    qtd_len_inicial = len(conteudo_alterado)
    qtd_len_final = 0
    while qtd_len_final < qtd_len_inicial:
        qtd_len_inicial = len(conteudo_alterado)
        conteudo_alterado = conteudo_alterado.replace('A PARTIR DE','A_PARTIR_DE')
        conteudo_alterado = conteudo_alterado.replace('– RECOMENDAÇÃO\n','– RECOMENDAÇÃO ')
        conteudo_alterado = conteudo_alterado.replace('REDE\nPÚBLICA','REDE PÚBLICA')
        conteudo_alterado = conteudo_alterado.replace('MÉDICO\nPERICIAL','MÉDICO PERICIAL')
        conteudo_alterado = conteudo_alterado.replace(' LICENÇA\nMÉDICA ',' LICENÇA MÉDICA ')
        conteudo_alterado = conteudo_alterado.replace(' DA LEI\n',' DA LEI ')
        conteudo_alterado = conteudo_alterado.replace(' P/ ',' PARA ')
        conteudo_alterado = conteudo_alterado.replace('RELAÇÃO DE CONCESSÃO DE NEXO DE ACIDENTE DO TRABALHO\n','RELAÇÃO DE CONCESSÃO DE NEXO DE ACIDENTE DO TRABALHO ')
        conteudo_alterado = conteudo_alterado.replace('RELAÇÃO DE SERVIDORES SUBMETIDOS À AVALIAÇÃO DE ESPECIALISTA COM CAPACIDADE LABORATIVA PARA A SUA FUNÇÃO\nORIGINAL','RELAÇÃO DE SERVIDORES SUBMETIDOS À AVALIAÇÃO DE ESPECIALISTA COM CAPACIDADE LABORATIVA PARA A SUA FUNÇÃO ORIGINAL')
        conteudo_alterado = conteudo_alterado.replace(' LICENÇAS\nMÉDICAS',' LICENÇAS MÉDICAS')
        conteudo_alterado = conteudo_alterado.replace('\nABAIXO',' ABAIXO')
        conteudo_alterado = conteudo_alterado.replace('ABAIXO\nIDENTIFICADO','ABAIXO IDENTIFICADO')
        conteudo_alterado = conteudo_alterado.replace('ABAIXO: ','ABAIXO:\n')
        conteudo_alterado = conteudo_alterado.replace('LICENÇA\n','LICENÇA ')
        conteudo_alterado = conteudo_alterado.replace('FUNÇÃO\nORIGINAL','FUNÇÃO ORIGINAL')
        conteudo_alterado = conteudo_alterado.replace('READAPTAÇÃO\nFUNCIONAL','READAPTAÇÃO FUNCIONAL')
        conteudo_alterado = conteudo_alterado.replace('PERÍCIA\nMÉDICA','PERÍCIA MÉDICA')
        conteudo_alterado = conteudo_alterado.replace('SERVIDORES COM LAUDO DE READAPTAÇÃO FUNCIONAL DEFERIDO POR ','SERVIDORES COM LAUDO DE READAPTAÇÃO FUNCIONAL DEFERIDO\nPOR ')
        conteudo_alterado = conteudo_alterado.replace('LICENÇA MÉDICA – RGPS, ','LICENÇA MÉDICA – RGPS\n')
        conteudo_alterado = conteudo_alterado.replace('LICENÇA MÉDICA – RGPS ','LICENÇA MÉDICA – RGPS\n')
        conteudo_alterado = conteudo_alterado.replace('LICENÇA MÉDICA – RECOMENDAÇÃO HSPM/HSPE/INSTITUIÇÕES PÚBLICAS DE SAÚDE ','LICENÇA MÉDICA – RECOMENDAÇÃO HSPM/HSPE/INSTITUIÇÕES PÚBLICAS DE SAÚDE\n')
        conteudo_alterado = conteudo_alterado.replace('LICENÇA MÉDICA-RGPS','LICENÇA MÉDICA – RGPS')
        conteudo_alterado = conteudo_alterado.replace('LICENÇAS MÉDICAS DO SERVIDOR - CONCEDIDAS NOS TERMOS DOARTIGO 143, DA LEI 8989/79, NA FORMA PREVISTA NO DECRETO NO 58.225/18,ARTIGO 38 INCISO II.','LICENÇAS MÉDICAS DO SERVIDOR - CONCEDIDAS NOS TERMOS DO ARTIGO 143, DA LEI 8989/79, NA FORMA PREVISTA NO DECRETO NO 58.225/18, ARTIGO 38 INCISO II.')
        conteudo_alterado = conteudo_alterado.replace('LICENÇA MÉDICA DO SERVIDOR - HSPM / HSPE / REDE PÚBLICA DE SAÙDE','LICENÇA MÉDICA DO SERVIDOR - HSPM/HSPE/REDE PÚBLICA DE SAÙDE')
        qtd_len_final = len(conteudo_alterado)
    print(f'Qtd de linhas depois: {len(conteudo_alterado)}')
    return conteudo_alterado

# %%
def limpa_secretarias(conteudo_alterado):
    print('### LIMPA SECRETARIAS ###')
    print(f'Qtd de linhas antes: {len(conteudo_alterado)}')
    conteudo_alterado = conteudo_alterado.replace('AGÊNCIA SÃO PAULO DE\nDESENVOLVIMENTO','AGÊNCIA SÃO PAULO DE DESENVOLVIMENTO')
    conteudo_alterado = conteudo_alterado.replace('AUTORIDADE MUNICIPAL DE LIMPEZA\nURBANA','AUTORIDADE MUNICIPAL DE LIMPEZA URBANA')
    conteudo_alterado = conteudo_alterado.replace('COMPANHIA DE ENGENHARIA DE\nTRAFEGO','COMPANHIA DE ENGENHARIA DE TRAFEGO')
    conteudo_alterado = conteudo_alterado.replace('COMPANHIA METROPOLITANA DE\nHABITAÇÃO','COMPANHIA METROPOLITANA DE HABITAÇÃO')
    conteudo_alterado = conteudo_alterado.replace('DESENVOLVIMENTO ECONÔMICO,\nTRABALHO E TURISMO','DESENVOLVIMENTO ECONÔMICO, TRABALHO E TURISMO')
    conteudo_alterado = conteudo_alterado.replace('EMPRESA DE CINEMA E AUDIOVISUAL\nDE SÃO PAULO','EMPRESA DE CINEMA E AUDIOVISUAL DE SÃO PAULO')
    conteudo_alterado = conteudo_alterado.replace('EMPRESA DE TECNOLOGIA DA\nINFORMAÇÃO E COMUNICAÇÃO','EMPRESA DE TECNOLOGIA DA INFORMAÇÃO E COMUNICAÇÃO')
    conteudo_alterado = conteudo_alterado.replace('ENGLOBAMENTO DE LICENÇAS MÉDICAS FACE PORTARIA\n11/84','ENGLOBAMENTO DE LICENÇAS MÉDICAS FACE PORTARIA 11/84')
    conteudo_alterado = conteudo_alterado.replace('FUNDAÇÃO PAULISTANA DE EDUCAÇÃO\nE TECNOLOGIA','FUNDAÇÃO PAULISTANA DE EDUCAÇÃO E TECNOLOGIA')
    conteudo_alterado = conteudo_alterado.replace('HOSPITAL DO SERVIDOR PÚBLICO\nMUNICIPAL','HOSPITAL DO SERVIDOR PÚBLICO MUNICIPAL')
    conteudo_alterado = conteudo_alterado.replace('SECRETARIA MUNICIPAL DAS\nSUBPREFEITURAS','SECRETARIA MUNICIPAL DAS SUBPREFEITURAS')
    print(f'Qtd de linhas depois: {len(conteudo_alterado)}')
    return conteudo_alterado

# %%
conteudo_alterado = limpa_tabulacao(conteudo_alterado)
conteudo_alterado = palavras_especificas(conteudo_alterado)
conteudo_alterado = limpa_tabulacao(conteudo_alterado)
conteudo_alterado = limpa_secretarias(conteudo_alterado)
conteudo_alterado = limpa_tabulacao(conteudo_alterado)
conteudo_alterado = normaliza_cabecalho(conteudo_alterado)
conteudo_alterado = limpa_tabulacao(conteudo_alterado)
conteudo_alterado = limpa_conjuncao_preposicao(conteudo_alterado)
conteudo_alterado = limpa_tabulacao(conteudo_alterado)
conteudo_alterado = palavras_especificas(conteudo_alterado)
print("#### Limpeza dos dados ####")

# %%
# Localiza o início das seções SERVIDORES e CONCURSOS
sc_servidores = conteudo_alterado.find('\nSERVIDORES\n')
sc_concursos = conteudo_alterado.find('\nCONCURSOS\n')
print(f"SERVIRODRES: {sc_servidores} / CONCURSOS: {sc_concursos}")
conteudo_servidores = conteudo_alterado[sc_servidores:sc_concursos]
#conteudo_servidores = conteudo

# %%
#print(conteudo_servidores)
save_file(SAVE_DIR,conteudo_servidores,'00-SECAO_SERVIDORES')

# %%
save_file(SAVE_DIR,conteudo,'00-CONTEUDO SEM TRATAMENTO')

# %%
#print(conteudo_servidores)

# %% [markdown]
# ### Relação de Licença Médica

# %% [markdown]
# #### CONTEÚDO PRINCIPAL

# %%
conteudo_licenca_medica = conteudo_servidores

# %% [markdown]
# #### LICENÇAS MAPEADAS

# %%
licencas_mapeadas = {
    'RELAÇÃO DE ADICIONAIS POR TEMPO DE SERVIÇO NOS TERMOS DO ARTIGO 112, DA LEI 8989/79':                  'RF NOME QQ DATA EH',
    'RELAÇÃO DE ALTA DE AT/DT CANCELADA EM FUNÇÃO DE:':                                                     'RF NOME A_PARITR_DE',
    'RELAÇÃO DE ALTAS DO ACIDENTE DO TRABALHO E DA DOENÇA DO TRABALHO':                                     'RF NOME A_PARTIR_DE',
    'RELAÇÃO DE ALTAS DO ACIDENTE DO TRABALHO E DA DOENÇA DO TRABALHO :':                                   'RF NOME A_PARTIR_DE',
    'RELAÇÃO DE CONCESSÃO DE NEXO DE ACIDENTE DO TRABALHO DEFERIDO':                                        'RF NOME A_PARTIR_DE',
    'RELAÇÃO DE CONCESSÃO DE NEXO DE ACIDENTE DO TRABALHO INDEFERIDO':                                      'RF NOME A_PARTIR_DE',
    'RELAÇÃO DE CONCESSÃO DE NEXO DE ACIDENTE DO TRABALHO DEFERIDO EM GRAU DE RECURSO':                     'RF NOME A_PARTIR_DE',
    'RELAÇÃO DE CONCESSÃO DE NEXO DE ACIDENTE DO TRABALHO INDEFERIDO':                                      'RF NOME A_PARTIR_DE',
    'RELAÇÃO DE CONVOCADOS PARA JUNTA DE AVALIAÇÃO DE INCAPACIDADE PERMANENTE PARA O TRABALHO':             'RF NOME DATA_HORARIO',
    'RELAÇÃO DE CONVOCADOS PARA JUNTA MÉDICA PARA FINS DE PENSÃO POR MORTE':                                'RF NOME DATA_HORARIO',
    'RELAÇÃO DE CONVOCADOS PARA JUNTA MÉDICA PARA FINS DE SALÁRIO FAMÍLIA':                                 'RF NOME DATA_HORARIO',
    'RELAÇÃO DE CONVOCADOS PARA PERÍCIA MÉDICA DE ISENÇÃO DE IMPOSTO DE RENDA':                             'RF NOME DATA_HORARIO',
    'RELAÇÃO DE FALTA DO SERVIDOR À PERÍCIA':                                                               'RF NOME A_PARTIR_DE ARTIGO',
    'RELAÇÃO DE FALTAS DOS CONVOCADOS PARA AVALIAÇÃO DE ESPECIALISTA':                                      'RF NOME A_PARITR_DE',
    'RELAÇÃO DE FALTAS DOS CONVOCADOS PARA AVALIAÇÃO DE ISENÇÃO DE IMPOSTO DE RENDA':                       'RF NOME A_PARITR_DE',
    'RELAÇÃO DE FALTAS DOS CONVOCADOS PARA JUNTA MÉDICA PARA FINS DE PENSÃO POR MORTE':                     'RF NOME A_PARITR_DE',
    'RELAÇÃO DE FALTAS DOS CONVOCADOS PARA JUNTA MÉDICA PARA FINS DE SALÁRIO FAMÍLIA':                      'RF NOME A_PARITR_DE',
    'RELAÇÃO DE LICENÇAS MÉDICAS CANCELADAS EM FUNÇÃO DE:':                                                  'RF NOME DIAS A_PARITR_DE ARTIGO',
    'RELAÇÃO DE LICENÇAS MÉDICAS NEGADAS NOS TERMOS DA LEI 8989/79':                                        'RF NOME A_PARTIR_DE ARTIGO',
    'RELAÇÃO DE LICENÇAS MÉDICAS NOS TERMOS DA LEI 8989/79':                                                'RF NOME DIAS A_PARTIR_DE ARTIGO',
    'RELAÇÃO DE LICENÇAS MÉDICAS RETIFICADAS EM FUNÇÃO DE:':                                                'RF NOME DIAS A_PARTIR_DE ARTIGO',
    'ENGLOBAMENTO DE LICENÇAS MÉDICAS FACE PORTARIA 11/84':                                                 'RF NOME DIAS A_PARTIR_DE ARTIGO',
    'RELAÇÃO DE SERVIDORES COM ALTERAÇÕES NAS DATAS DE ATENDIMENTO PARA AVALIAÇÃO MÉDICA DE ACIDENTE DE TRABALHO': 'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES CONVOCADOS PARA AVALIAÇÃO COM ESPECIALISTA PARA READAPTAÇÃO/RESTRIÇÃO FUNCIONAL':'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES CONVOCADOS PARA AVALIAÇÃO MÉDICA DE ACIDENTE DE TRABALHO':                       'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES CONVOCADOS PARA AVALIAÇÃO MÉDICO PERICIAL':                                      'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES CONVOCADOS PARA AVALIAÇÃO COM MÉDICO PERITO ESPECIALISTA':                       'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES CONVOCADOS PARA JUNTA MÉDICA DE APOSENTADORIA POR INVALIDEZ':                    'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES CONVOCADOS PARA PERÍCIA DE RECONSIDERAÇÃO DE LICENÇA MÉDICA':                    'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES CONVOCADOS PARA PERÍCIA DE LICENÇA MÉDICA PRÓPRIO SERVIDOR - LONGA DURACAO':     'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES CONVOCADOS PARA RETORNO NA AVALIAÇÃO MÉDICA DE ACIDENTE DE TRABALHO':            'NOME RF DATA_HORARIO',
    'RELAÇÃO DE SERVIDORES SUBMETIDOS À AVALIAÇÃO DE CAPACIDADE LABORATIVA COM CAPACIDADE LABORATIVA PARA A SUA FUNÇÃO':        'RF NOME',
    'RELAÇÃO DE SERVIDORES SUBMETIDOS À AVALIAÇÃO DE CAPACIDADE LABORATIVA COM CAPACIDADE LABORATIVA PARA A SUA FUNÇÃO ORIGINAL':'RF NOME',
    'RELAÇÃO DE SERVIDORES SUBMETIDOS À AVALIAÇÃO DE ESPECIALISTA COM CAPACIDADE LABORATIVA PARA A SUA FUNÇÃO DE READAPTADO':   'RF NOME',
    'RELAÇÃO DE SERVIDORES SUBMETIDOS À AVALIAÇÃO DE ESPECIALISTA COM CAPACIDADE LABORATIVA PARA A SUA FUNÇÃO ORIGINAL':        'RF NOME A_PARTIR_DE ARTIGO',
    'SERVIDORES COM LAUDO DE READAPTAÇÃO FUNCIONAL CESSADO A PEDIDO DO SERVIDOR':                           'RF NOME',
    'SERVIDORES COM LAUDO DE READAPTAÇÃO FUNCIONAL DEFERIDO':                                               'RF NOME',
    'SERVIDORES COM LAUDO DE READAPTAÇÃO FUNCIONAL DEFINITIVO POR ACIDENTE DO TRABALHO A_PARTIR_DE':        'RF NOME A_PARTIR_DE',
    'LICENÇA MÉDICA – SERVIDOR FILIADO AO RGPS':                                                            'LICENÇA MÉDICA RGPS',
    'LICENÇA MÉDICA – RECOMENDAÇÃO HSPM/HSPE/INSTITUIÇÕES PÚBLICAS DE SAÚDE':                               'LICENÇA MÉDICA RGPS',
    'LICENÇA MÉDICA – RGPS':                                                                                'LICENÇA MÉDICA RGPS',
    'LICENÇA MÉDICA DE ATÉ 15 DIAS PARA O SERVIDOR.':                                                       'LICENÇA MÉDICA RGPS',
    'LICENÇA MÉDICA DE CURTA DURACAO':                                                                      'LICENÇA MÉDICA RGPS',
    'LICENÇA MÉDICA DE CURTA DURACAO - RECOMENDAÇÃO HSPM/HSPE/INSTITUIÇÕES PÚBLICAS DE SAÚDE':              'LICENÇA MÉDICA RGPS',
    'LICENÇA MÉDICA DO SERVIDOR – RECOMENDAÇÃO HSPM':                                                       'LICENÇA MÉDICA RGPS',
    'LICENÇA MÉDICA DO SERVIDOR – RECOMENDAÇÃO UNIDADES PUBLICAS':                                          'LICENÇA MÉDICA RGPS',
    'LICENÇA MÉDICA DO SERVIDOR – RECOMENDAÇÃO DAS UNIDADES PÚBLICAS DE SAÚDE':                             'RF NOME A_PARTIR_DE',
    'LICENÇA MÉDICA DO SERVIDOR - HSPM/HSPE/REDE PÚBLICA DE SAÙDE':                                         'LICENÇA MÉDICA RGPS',
    'LICENÇA GALA':                                                                                         'RF NOME DIAS A_PARTIR_DE',
    #'LICENÇA NOJO':                                                                                         'LICENCA_NOJO',
    'LICENÇAS MÉDICAS CONCEDIDAS/NEGADAS EM GRAU DE RECURSO':                                               'RF NOME DIAS A_PARTIR_DE ARTIGO',
    'LICENÇAS MÉDICAS DE CURTA DURACAO':                                                                    'LICENÇA MÉDICA RGPS',
    'LICENÇAS MÉDICAS DO SERVIDOR - CONCEDIDAS NOS TERMOS DO ARTIGO 143, DA LEI 8989/79, NA FORMA PREVISTA NO DECRETO NO 58.225/18, ARTIGO 38 INCISO II.':'LICENÇA MÉDICA RGPS',
    'LICENÇAS MÉDICAS DOS SERVIDORES-RECOMENDAÇÃO DO HSPM.':                                                'LICENÇA MÉDICA RGPS',
    'LICENÇAS MÉDICAS DOS SERVIDORES-RECOMENDAÇÃO DA REDE PÚBLICA.':                                        'LICENÇA MÉDICA RGPS',
    'LICENÇAS MÉDICAS PARA SERVIDORES SOB REGIME GERAL DA PREVIDÊNCIA SOCIAL':                              'LICENÇA MÉDICA RGPS',
}

# %% [markdown]
# #### LICENÇAS MÉDICAS

# %%
rl_lm =  conteudo_licenca_medica.split('\n')
str_listagens = 'ID;LISTAGEM;INICIO;MAPEADA;QTD\n'
linha = 0
lin_anterior = 0
id = 0
listas = []

for line in rl_lm:
    mapeada = line in licencas_mapeadas
    if ('LICENÇAS MÉDICAS' in line or 'LICENÇA NOJO' in line or 'LICENÇA GALA' in line or 'LICENÇA MÉDICA' in line ) and not ('SEÇÃO DE LICENÇAS MÉDICAS' in line or 'ENGLOBAMENTO DE L' in line):
        id += 1
        listas.append(linha)
        if id == 1:
            str_listagens += f'{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        if id > 1:
            qtd = linha - lin_anterior
            str_listagens += f'{qtd}\n{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        #print(line)
    elif ('RELAÇÃO DE' in line or 'RELAÇÃO DOS' in line):
        id += 1
        listas.append(linha)
        if id == 1:
            str_listagens += f'{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        if id > 1:
            qtd = linha - lin_anterior
            str_listagens += f'{qtd}\n{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        #print(line)
    elif 'SERVIDORES COM' in line or 'NOMES DOS SERVIDORES' in line or 'SERVIDOR(ES) ABAIXO' in line:
        id += 1
        listas.append(linha)
        if id == 1:
            str_listagens += f'{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        if id > 1:
            qtd = linha - lin_anterior
            str_listagens += f'{qtd}\n{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        #print(line)
    elif 'HORÁRIO AMAMENTAÇÃO – DEFERIDO' in line or 'FÉRIAS DEFERIDAS' in line:
        id += 1
        listas.append(linha)
        if id == 1:
            str_listagens += f'{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        if id > 1:
            qtd = linha - lin_anterior
            str_listagens += f'{qtd}\n{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        #print(line)
    elif 'DESPACHOS' in line:
        id += 1
        listas.append(linha)
        if id == 1:
            str_listagens += f'{id};{line};{linha};{mapeada};'
            lin_anterior = linha
        if id > 1:
            qtd = linha - lin_anterior
            str_listagens += f'{qtd}\n{id};{line};{linha};{mapeada};'
            lin_anterior = linha
    elif linha == len(rl_lm) - 1:
        str_listagens += f'{qtd}'

    #if 'RF' in line or 'REG. FUN.' in line or 'REG.FUN.' in line:
        #print(line)
    linha += 1

#print(licencas)
#print(OrderedDict(licencas))
#print(listas)
print(str_listagens)
print(f'\nTotal de listas: {len(listas)}')
save_file(SAVE_DIR,str_listagens,'00-LISTAGENS_DOM','csv')

# %% [markdown]
# ##### VALIDAR LISTA

# %%
def qual_script(RELACAO,SCRIPT,LISTA):
    LISTA_ARRUMADA = ''
    if SCRIPT == 'EH_RF_NOME_DIAS_A_PARTIR_DE':
        LISTA_ARRUMADA = EH_RF_NOME_DIAS_A_PARTIR_DE(RELACAO,LISTA)
    elif SCRIPT == 'NOME RF DATA_HORARIO':
        LISTA_ARRUMADA = NOME_RF_DATA_HORARIO(RELACAO,LISTA)
    elif SCRIPT == 'RF NOME QQ DATA EH':
        LISTA_ARRUMADA = RF_NOME_QQ_DATA_EH(RELACAO,LISTA)
    elif SCRIPT == 'RF NOME DIAS A_PARTIR_DE ARTIGO':
        LISTA_ARRUMADA = RF_NOME_DIAS_A_PARTIR_DE_ARTIGO(RELACAO,LISTA)
    elif SCRIPT == 'RF NOME DIAS A_PARTIR_DE':
        LISTA_ARRUMADA = RF_NOME_DIAS_A_PARTIR_DE(RELACAO,LISTA)
    elif SCRIPT == 'RF NOME A_PARTIR_DE ARTIGO':
        LISTA_ARRUMADA = RF_NOME_A_PARTIR_DE_ARTIGO(RELACAO,LISTA)
    elif SCRIPT == 'RF NOME A_PARTIR_DE':
        LISTA_ARRUMADA = RF_NOME_A_PARTIR_DE(RELACAO,LISTA)
    elif SCRIPT == 'RF NOME PERIODO':
        LISTA_ARRUMADA = RF_NOME_PERIODO(RELACAO,LISTA)
    elif SCRIPT == 'RF NOME':
        LISTA_ARRUMADA = RF_NOME(RELACAO,LISTA)
    elif SCRIPT == 'LICENÇA MÉDICA RGPS':
        LISTA_ARRUMADA = LICENÇA_MEDICA_SERVIDOR_FILIADO_AO_RGPS(RELACAO,LISTA)
    #elif SCRIPT == 'LICENCA_NOJO':
    #    LISTA_ARRUMADA = LICENCA_NOJO(RELACAO,LISTA)
    if not LISTA_ARRUMADA == '':
        RELACAO = str('_').join(RELACAO.replace('/','_').replace(',','_').replace(':','_').split(' '))
        add_file(SAVE_DIR,LISTA_ARRUMADA,RELACAO,'csv')
    return LISTA_ARRUMADA


# %% [markdown]
# ##### EH RF NOME DIAS A_PARTIR_DE

# %%
def EH_RF_NOME_DIAS_A_PARTIR_DE(RELACAO,list_items):
    '''
        COLUNAS:
            1. EH           : numeric()  s_item[0]
            2. RF           : numeric(7) s_item[1][0]
            3. VINC         : numeric(1) s_item[1][1]
            4. NOME         : str()      s_item[2:-2]
            5. DIAS         : numeric()  s_item[-2]
            6. A_PARTIR_DE  : date()     s_item[-1]
    '''
    i = 0
    SECRETARIA = ''
    VALIDA_LINHA = ''
    print(RELACAO)

    str_list_items = 'EH;RF;VINC;NOME;DIAS;A_PARTIR_DE;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        s_item = item.strip().split(' ')
        #print(f'analise: {s_item}')
        if 'EH RF' in item:
            SECRETARIA = list_items[i-1]
        elif len(s_item) >= 7:
            if len(s_item) >= 7 and s_item[0][0].isnumeric() and s_item[1][0].isnumeric() and s_item[-2][0].isnumeric() and s_item[-1][0].isnumeric():
                eh = s_item[0]
                if len(s_item[1].split('/')) >= 2:
                    rf = s_item[1].split('/')[0].replace('.','')
                    vinc = s_item[1].split('/')[1]
                else:
                    rf = s_item[1].split('/')[0]
                    vinc = 0
                nome = str(' ').join(s_item[2:-2])
                dias = s_item[-2]
                a_partir_de = s_item[-1]
                str_list_items += f'{eh};{rf};{vinc};{nome};{dias};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
                #print(str_list_items)
        elif len(s_item) >= 5 and s_item[0][-1].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            eh = s_item[0]
            rf = s_item[1].split('/')[0].replace('.','')
            vinc = s_item[1].split('/')[1]
            nome = str(' ').join(s_item[2:-2])
            dias = s_item[-2]
            a_partir_de = s_item[-1]
            str_list_items += f'{eh};{rf};{vinc};{nome};{dias};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items

# %% [markdown]
# ##### RF NOME QQ DATA EH

# %%
def RF_NOME_QQ_DATA_EH(RELACAO,list_items):
    '''Listagem: RELAÇÃO DE LICENÇAS MÉDICAS NOS TERMOS DA LEI 8989/79
    COLUNAS:
        1. RF           : numeric(7) s_item[0][0]
        2. VINC         : numeric(1) s_item[0][1]
        3. NOME         : str()      s_item[2:-3]
        4. QQ           : numeric()  s_item[-3]
        5. DATA         : date()     s_item[-2]
        6. EH           : str()      s_item[-1]
'''
    i = 0
    SECRETARIA = ''
    VALIDA_LINHA = ''
    print(RELACAO)
    str_list_items = 'RF;VINC;NOME;QQ;DATA;EH;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        s_item = item.strip().split(' ')
        #print(f'analise: {s_item}')
        if 'RF NOME' in item:
            SECRETARIA = list_items[i-1]
        elif len(s_item) >= 5:
            if len(s_item) >= 5 and s_item[0][0].isnumeric() and s_item[-3][0].isnumeric() and s_item[-2][0].isnumeric() and s_item[0].find('/') != -1:
                if len(s_item[0].split('/')) >= 2:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = s_item[0].split('/')[1]
                else:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = 0
                nome = str(' ').join(s_item[1:-3])
                str_list_items += f'{rf};{vinc};{nome};{s_item[-3]};{s_item[-2]};{s_item[-1]};{SECRETARIA};{RELACAO};{DOM}\n'
                #print(str_list_items)
        elif len(s_item) >= 2 and s_item[0][-1].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            rf = s_item[0].split('/')[0]
            vinc = s_item[0].split('/')[1]
            nome = str(' ').join(s_item[1:-3])
            str_list_items += f'{rf};{vinc};{nome};{s_item[-3]};{s_item[-2]};{s_item[-1]};{SECRETARIA};{RELACAO};{DOM}\n'
            print(str_list_items)
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items


# %% [markdown]
# ##### NOME RF DATA_HORARIO

# %%
def NOME_RF_DATA_HORARIO(RELACAO,list_items):
    '''
    COLUNAS:
        1. NOME             : numeric(7) s_item[0:-3]
        2. RF               : numeric(1) s_item[-3]
        3. DATA             : date()     s_item[-2]
        4. HORARIO          : numeric()  s_item[-1]
'''
    i = 0
    SECRETARIA = ''
    VALIDA_LINHA = ''
    print(RELACAO)

    str_list_items = 'NOME;RF;VINCULO;DATA;HORARIO;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        s_item = item.strip().split(' ')
        #print(f'analise: {s_item}')
        if 'NOME RF DATA_HORARIO' in item:
            SECRETARIA = list_items[i-1]
        elif len(s_item) >= 5:
            if len(s_item) >= 5 and s_item[-3][0].isnumeric() and s_item[-2][0].isnumeric() and s_item[-1][0].isnumeric():
                nome = str(' ').join(s_item[0:-3])
                if len(s_item[-3].split('/')) >= 2:
                    rf = s_item[-3].split('/')[0].replace('.','')
                    vinc = s_item[-3].split('/')[1]
                else:
                    rf = s_item[-3].split('/')[0].replace('.','')
                    vinc = 0
                rf = s_item[-3].replace('.','')
                data = s_item[-2]
                horario = s_item[-1]
                str_list_items += f'{nome};{rf};{vinc};{data};{horario};{SECRETARIA};{RELACAO};{DOM}\n'
                #print(str_list_items)
        elif len(s_item) >= 2 and s_item[-1][0].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            nome = str(' ').join(s_item[0:-3])
            rf = s_item[-3]
            data = s_item[-2]
            horario = s_item[-1]
            str_list_items += f'{nome};{rf};{data};{horario};{SECRETARIA};{RELACAO};{DOM}\n'
            #print(str_list_items)
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items


# %% [markdown]
# ##### RF NOME DIAS A_PARTIR_DE ARTIGO

# %%
def RF_NOME_DIAS_A_PARTIR_DE_ARTIGO(RELACAO,list_items):
    '''
        COLUNAS:
            1. RF           : numeric(7) s_item[0][0]
            2. VINC         : numeric(1) s_item[0][1]
            3. NOME         : str()      s_item[2:-3]
            4. DIAS         : numeric()  s_item[-3]
            5. A_PARTIR_DE  : date()     s_item[-2]
            6. ARTIGO       : str()      s_item[-1]
    '''
    i = 0
    SECRETARIA = ''
    VALIDA_LINHA = ''
    print(RELACAO)

    str_list_items = 'RF;VINC;NOME;DIAS;A_PARTIR_DE;ARTIGO;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        s_item = item.strip().split(' ')
        #print(f'analise: {s_item}')
        if 'RF NOME' in item:
            SECRETARIA = list_items[i-1]
        elif len(s_item) >= 6:
            if len(s_item) >= 6 and s_item[0][0].isnumeric() and s_item[-2][0].isnumeric():
                if len(s_item[0].split('/')) >= 2:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = s_item[0].split('/')[1]
                else:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = 0
                nome = str(' ').join(s_item[1:-3])
                dias = s_item[-3]
                a_partir_de = s_item[-2]
                artigo = s_item[-1]
                str_list_items += f'{rf};{vinc};{nome};{dias};{a_partir_de};{artigo};{SECRETARIA};{RELACAO};{DOM}\n'
                #print(str_list_items)
        elif len(s_item) >= 5 and s_item[0][-1].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            rf = s_item[0].split('/')[0]
            vinc = s_item[0].split('/')[1]
            nome = str(' ').join(s_item[1:-3])
            dias = s_item[-3]
            a_partir_de = s_item[-2]
            artigo = s_item[-1]
            str_list_items += f'{rf};{vinc};{nome};{dias};{a_partir_de};{artigo};{SECRETARIA};{RELACAO};{DOM}\n'
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items

# %% [markdown]
# ##### RF NOME DIAS A_PARTIR_DE

# %%
def RF_NOME_DIAS_A_PARTIR_DE(RELACAO,list_items):
    '''
        COLUNAS:
            1. RF           : numeric(7) s_item[0][0]
            2. VINC         : numeric(1) s_item[0][1]
            3. NOME         : str()      s_item[1:-2]
            4. DIAS         : numeric()  s_item[-2]
            5. A_PARTIR_DE  : date()     s_item[-1]
    '''
    i = 0
    SECRETARIA = ''
    VALIDA_LINHA = ''
    print(RELACAO)

    str_list_items = 'RF;VINC;NOME;DIAS;A_PARTIR_DE;ARTIGO;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        s_item = item.strip().split(' ')
        #print(f'analise: {s_item}')
        if 'RF NOME' in item:
            SECRETARIA = list_items[i-1]
        elif len(s_item) >= 6:
            if len(s_item) >= 6 and s_item[0][0].isnumeric() and s_item[-2][0].isnumeric() and s_item[-1][0].isnumeric():
                if len(s_item[0].split('/')) >= 2:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = s_item[0].split('/')[1]
                else:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = 0
                nome = str(' ').join(s_item[1:-3])
                dias = s_item[-3]
                a_partir_de = s_item[-2]
                artigo = s_item[-1]
                str_list_items += f'{rf};{vinc};{nome};{dias};{a_partir_de};{artigo};{SECRETARIA};{RELACAO};{DOM}\n'
                #print(str_list_items)
        elif len(s_item) >= 5 and s_item[0][-1].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            rf = s_item[0].split('/')[0]
            vinc = s_item[0].split('/')[1]
            nome = str(' ').join(s_item[1:-3])
            dias = s_item[-3]
            a_partir_de = s_item[-2]
            artigo = s_item[-1]
            str_list_items += f'{rf};{vinc};{nome};{dias};{a_partir_de};{artigo};{SECRETARIA};{RELACAO};{DOM}\n'
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items

# %% [markdown]
# ##### RF NOME A_PARTIR_DE ARTIGO

# %%
def RF_NOME_A_PARTIR_DE_ARTIGO(RELACAO,list_items):
    '''
        COLUNAS:
            1. RF           : numeric(7) s_item[0][0]
            2. VINC         : numeric(1) s_item[0][1]
            3. NOME         : str()      s_item[1:-2]
            4. A_PARTIR_DE  : date()     s_item[-2]
            5. ARTIGO       : str()      s_item[-1]
    '''
    i = 0
    SECRETARIA = ''
    VALIDA_LINHA = ''
    print(RELACAO)

    str_list_items = 'RF;VINC;NOME;A_PARTIR_DE;ARTIGO;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        s_item = item.strip().split(' ')
        #print(f'analise: {s_item}')
        if 'RF NOME' in item:
            SECRETARIA = list_items[i-1]
        elif len(s_item) >= 5:
            if len(s_item) >= 5 and s_item[0][0].isnumeric() and s_item[-2][0].isnumeric():
                if len(s_item[0].split('/')) >= 2:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = s_item[0].split('/')[1]
                else:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = 0
                nome = str(' ').join(s_item[1:-3])
                a_partir_de = s_item[-2]
                artigo = s_item[-1]
                str_list_items += f'{rf};{vinc};{nome};{a_partir_de};{artigo};{SECRETARIA};{RELACAO};{DOM}\n'
                #print(str_list_items)
        elif len(s_item) >= 2 and s_item[0][-1].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            rf = s_item[0].split('/')[0]
            vinc = s_item[0].split('/')[1]
            nome = str(' ').join(s_item[1:-3])
            a_partir_de = s_item[-2]
            artigo = s_item[-1]
            str_list_items += f'{rf};{vinc};{nome};{a_partir_de};{artigo};{SECRETARIA};{RELACAO};{DOM}\n'
            print(str_list_items)
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items

# %% [markdown]
# ##### RF NOME A_PARTIR_DE

# %%
def RF_NOME_A_PARTIR_DE(RELACAO,list_items):
    '''
        COLUNAS:
            1. RF           : numeric(7) s_item[0][0]
            2. VINC         : numeric(1) s_item[0][1]
            3. NOME         : str()      s_item[1:-1]
            4. A_PARTIR_DE  : date()     s_item[-1]
    '''
    i = 0
    SECRETARIA = ''
    VALIDA_LINHA = ''
    print(RELACAO)

    str_list_items = 'RF;VINC;NOME;A_PARTIR_DE;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        s_item = item.strip().split(' ')
        #print(f'analise: {s_item}')
        if 'RF NOME' in item:
            SECRETARIA = list_items[i-1]
        elif len(s_item) >= 5:
            if len(s_item) >= 5 and s_item[0][0].isnumeric() and s_item[-1][0].isnumeric():
                if len(s_item[0].split('/')) >= 2:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = s_item[0].split('/')[1]
                else:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = 0
                nome = str(' ').join(s_item[1:-1])
                a_partir_de = s_item[-1]
                str_list_items += f'{rf};{vinc};{nome};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
                #print(str_list_items)
        elif len(s_item) >= 2 and s_item[0][-1].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            rf = s_item[0].split('/')[0]
            vinc = s_item[0].split('/')[1]
            nome = str(' ').join(s_item[1:-1])
            a_partir_de = s_item[-1]
            str_list_items += f'{rf};{vinc};{nome};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
            #print(str_list_items)
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items

# %% [markdown]
# ##### RF NOME PERIODO

# %%
def RF_NOME_PERIODO(RELACAO,list_items):
    '''
        COLUNAS:
            1. RF           : numeric(7) s_item[0][0]
            2. VINC         : numeric(1) s_item[0][1]
            3. NOME         : str()      s_item[1:-1]
            4. A_PARTIR_DE  : date()     s_item[-1]
    '''
    i = 0
    SECRETARIA = ''
    VALIDA_LINHA = ''
    print(RELACAO)

    str_list_items = 'RF;VINC;NOME;A_PARTIR_DE;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        #print(item)
        s_item = item.strip().replace('.','').split(' ')
        #print(f'analise: {s_item}')
        if 'RF NOME' in item:
            SECRETARIA = list_items[i-1]
        elif len(s_item) >= 4:
            if len(s_item) >= 4 and s_item[0][0].isnumeric() and s_item[0].find('/') != -1:
                if len(s_item[0].split('/')) >= 2:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = s_item[0].split('/')[1]
                else:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = 0
                nome = str(' ').join(s_item[1:-1])
                a_partir_de = s_item[-1]
                str_list_items += f'{rf};{vinc};{nome};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
                #print(str_list_items)
        elif len(s_item) >= 2 and s_item[0][-1].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            rf = s_item[0].split('/')[0]
            vinc = s_item[0].split('/')[1]
            nome = str(' ').join(s_item[1:-1])
            a_partir_de = s_item[-1]
            str_list_items += f'{rf};{vinc};{nome};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
            #print(str_list_items)
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items

# %% [markdown]
# ##### RF NOME

# %%
def RF_NOME(RELACAO,list_items):
    '''
        COLUNAS:
            1. RF           : numeric(7) s_item[0][0]
            2. VINC         : numeric(1) s_item[0][1]
            3. NOME         : str()      s_item[-1]
    '''
    i = 0
    SECRETARIA = ''
    periodo = ''
    VALIDA_LINHA = ''
    list_items = str('\n').join(list_items).replace(' POR ','\nPOR ').split('\n')
    print(RELACAO)
    print(list_items)

    str_list_items = 'RF;VINCULO;NOME;PERIODO;A_PARTIR_DE;SECRETARIA;LISTA;DOM\n'

    for item in list_items:
        #print(item)
        s_item = item.strip().replace('.','').split(' ')
        #print(f'analise: {s_item}')
        if 'RF NOME' in item:
            SECRETARIA = list_items[i-1]
        elif 'POR ' in item or 'A_PARTIR_DE' in item:
            periodo = item
        elif len(s_item) >= 3:
            if len(s_item) >= 3 and s_item[0][0].isnumeric() and s_item[0].find('/') != -1:
                if len(s_item[0].split('/')) >= 2:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = s_item[0].split('/')[1]
                else:
                    rf = s_item[0].split('/')[0].replace('.','')
                    vinc = 0
                if '/' in s_item[-1]:
                    a_partir_de = s_item[-1]
                    nome = str(' ').join(s_item[1:-1])
                    str_list_items += f'{rf};{vinc};{nome};{periodo};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
                else:
                    a_partir_de = ''
                    nome = str(' ').join(s_item[1:])
                    str_list_items += f'{rf};{vinc};{nome};{periodo};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
                    #print(str_list_items)
        elif len(s_item) >= 2 and s_item[0][-1].isnumeric() and VALIDA_LINHA == False:
            linha = s_item
            VALIDA_LINHA = True
        elif VALIDA_LINHA == True:
            linha += f' {item}'
            s_item = item.split(' ')
            rf = s_item[0].split('/')[0]
            vinc = s_item[0].split('/')[1]
            nome = str(' ').join(s_item[1:-1])
            a_partir_de = s_item[-1]
            str_list_items += f'{rf};{vinc};{nome};{a_partir_de};{SECRETARIA};{RELACAO};{DOM}\n'
            #print(str_list_items)
            VALIDA_LINHA = False
        i += 1
        #print(i)
    return str_list_items

# %% [markdown]
# ##### LICENÇA NOJO

# %%
def LICENCA_NOJO(RELACAO,list_items):
    for item in list_items:
        if 'RF NOME PERIODO' in item:
            str_list_items = RF_NOME_PERIODO(RELACAO,list_items)

    return str_list_items

# %% [markdown]
# ##### LICENÇA MÉDICA – SERVIDOR FILIADO AO RGPS

# %%
def LICENÇA_MEDICA_SERVIDOR_FILIADO_AO_RGPS(RELACAO,list_items):
    print(RELACAO)
    print(list_items)
    for item in list_items:
        if 'EH RF/VINCULO NOME DURACAO A_PARTIR_DE' in item:
            str_list_items = EH_RF_NOME_DIAS_A_PARTIR_DE(RELACAO,list_items)
        elif 'RF NOME DURACAO A_PARTIR_DE' in item:
            str_list_items = RF_NOME_DIAS_A_PARTIR_DE(RELACAO,list_items)
        else:
            str_list_items = ''
    return str_list_items

# %% [markdown]
# ##### PESQUISA LISTA

# %%
for lista in str_listagens.split('\n')[1:]:
    id = lista.split(';')[0]
    relacao = lista.split(';')[1]
    inicio = int(lista.split(';')[-3])
    #inicio = (lista.split(';')[-3])
    mapeada = lista.split(';')[-2]
    qtd = int(lista.split(';')[-1])
    #qtd = (lista.split(';')[-1])
    fim = int(inicio + qtd)
    #fim = (inicio + qtd)
    lista = rl_lm[inicio:fim]
    script = licencas_mapeadas.get(relacao)
    LISTA_ARRUMADA = qual_script(relacao,script,lista)
    

# %%
!mkdir P:\00-D.O.M-SP\{dt_now}

# %%
!copy C:\Projetos\scrapy_dom\outputs_files\{dt_now}\  P:\00-D.O.M-SP\{dt_now}

# %%
!mkdir P:\00-D.O.M-SP\{dt_now}\todas_paginas

# %%
!copy C:\Projetos\scrapy_dom\querido-diario\data_collection\data\3550308\{dt_now}\  P:\00-D.O.M-SP\{dt_now}\todas_paginas

# %%
!dir P:\00-D.O.M-SP

# %%


# %% [markdown]
# ## Enviar e-mail com os dados

# %%
from email.message import EmailMessage
import smtplib

# %%
EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('SENHA')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')

# %%
# configurações principais
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
EMAIL_SUBJECT = "Teste Python"
#EMAIL_MESSAGE = "The message here"
EMAIL_MESSAGE = f"""
<p>Olá Lira, aqui é o código Python</p>

<p>O faturamento da loja foi de R$</p>
<p>Vendemos produtos</p>
<p>O ticket Médio foi de R$</p>

<p>Abs,</p>
<p>Código Python</p>
"""

# %%
msg = EmailMessage()
msg['Subject'] = EMAIL_SUBJECT
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO
msg.set_content(EMAIL_MESSAGE)
msg.add_alternative("""
<!DOCTYPE html>
<html>
    <body>
        <h1 style="color:MidnightBlue;">Email escrito em HTML!</h1>
    </body>
</html>
""", subtype='html')
msg.add_alternative("""
<!DOCTYPE html>
<html>
    <body>
        <p><strong>*MENSAGEM AUTOMÁTICA</strong><br>
        <br>
        Prezado(a) @{triggerOutputs()?['body/Title']},<br>
        <br>
        Agradecemos o seu contato. Sua documentação foi recebida com sucesso, conforme abaixo:<br>
        <br>
        <strong>Forma de entrega:</strong> @{triggerOutputs()?['body/TIPO_DE_ENTREGA/Value']}<br>
        <strong>CPF:</strong> @{triggerOutputs()?['body/CPF/Value']}<br>
        <strong>RG:</strong> @{triggerOutputs()?['body/RG/Value']}<br>
        <strong>Holerite:</strong> @{triggerOutputs()?['body/HOLERITE/Value']}<br>
        <strong>Comprovante de residência:</strong> @{triggerOutputs()?['body/COMPROVANTE_DE_RESIDENCIA/Value']}<br>
        <br>
        Futuramente entraremos em contato para mais informações e próximos passos, aguarde novo contato.<br>
        <br>
        <hr>
        <strong>Sindicato dos Trabalhadores na Administração Pública e Autarquias no Município de São Paulo – SINDSEP-SP<br>
        Endereço: </strong>Rua da Quitanda, 101, Centro, São Paulo SP | <a href="https://www.google.com/maps/place/Sindsep+-+Sindicato+dos+Servidores+Municipais+de+S%C3%A3o+Paulo/@-23.547807,-46.6374145,17z/data=!3m1!4b1!4m5!3m4!1s0x94ce5854be954cbd:0x10d8943160d93ef!8m2!3d-23.5478119!4d-46.6352258"><u><strong>veja no mapa</strong></u></a><br>
        <strong>e-mail para contato:</strong> <a href="mailto:coletivas@sindsep-sp.org.br">coletivas@sindsep-sp.org.br</a><br>
        <strong>Site:</strong> www.sindsep-sp.org.br |<strong> </strong><a href="https://sindsep-sp.org.br/" target="blank"><u><strong>acesse aqui</strong></u></a><br>
        <br>
        <em><strong>O SINDSEP, se compromete a tratar os dados nos termos da Lei Geral de Proteção de Dados Pessoais e em conformidade com a “Política de Privacidade” disponível no site do SINDSEP-SP.</strong></em> <a href="https://sindsep-sp.org.br/institucional/politica-de-privacidade" target="blank"><u><strong>Leia aqui.</strong></u></a></p>
    </body>
</html>
""", subtype='html')
#anexo = DATA_FILE
#msg.add_attachment(anexo)

# %%
files = os.listdir(SAVE_DIR)

for file in files:
    with open(f"{SAVE_DIR}\\{file}", 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, 
        maintype='application', 
        subtype='octet-stream',
        filename=file_name
    )

# %%
files

# %%
smtp = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)

# %%
smtp.starttls()

# %%
smtp.login(SMTP_USERNAME,SMTP_PASSWORD)

# %%
message = 'Subject: {}\n\n{}'.format(EMAIL_SUBJECT, EMAIL_MESSAGE)

# %%
email_enviado = smtp.send_message(msg)

# %%
email_enviado

# %%
smtp.quit()

# %%


# %%


# %%


# %%


# %%



