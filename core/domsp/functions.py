'''
Funções principais utilizadas na class domsp
'''

import subprocess
import re
import random
import chardet
from functools import reduce
from datetime import datetime, timedelta, date
from time import time

import fitz as fz
from pandas import read_csv, concat
from PyPDF2 import PdfFileReader, PdfFileMerger
from tabula import convert_into_by_batch

from scripts.limpeza_dados import limpa_dados, limpa_dados_preposicao_conjuncao
from scripts.listagens.servidores import limpa_dados_servidores

# CONSTANTES E VARIÁVEIS
CABECALHO_DOM = re.compile(r'((\d+) \W )?(São Paulo, (\d+) \((\d+)\))( \W (\d+))?')

def houve_publicacao(published):
    '''Obtém a data atual e retorna uma string: (YYYY-mm-dd)'''
    base = subprocess.os.getcwd()
    subprocess.os.chdir(base)
    feriadosmunicipais = read_csv(subprocess.os.path.join(base,'core','Feriados','docs','FeriadosMunicipaisBr.csv'),sep=';').query('UF == "SP" and NOME_DA_CIDADE == "São Paulo"')[['UF','NOME_DA_CIDADE','DIA','MÊS']]
    feriadosmunicipais['EVENTO'] = 'Aniversário do Município de São Paulo'
    feriadosestaduais = read_csv(subprocess.os.path.join(base,'core','Feriados','docs','FeriadosEstaduaisBr.csv'),sep=';').query('UF == "SP"')
    feriadosnacionais = read_csv(subprocess.os.path.join(base,'core','Feriados','docs','FeriadosNacionaisBr.csv'),sep=';')
    feriados = concat([feriadosmunicipais,feriadosestaduais,feriadosnacionais],ignore_index=True)
    
    while True:
        if feriados.query(f'DIA == {published.day} and MÊS == {published.month}')['EVENTO'].count() != 0:
            published = published - timedelta(1)
            print("ATENÇÃO: Não houve publicação neste dia. FERIADO na data de solicitação. Data de solicitação ajustada para a última publicação.")
            published = houve_publicacao(published)
        elif (published.weekday() == 0 or published.weekday() == 6) and published <= datetime.now().date():
            if published.weekday() == 0:
                published = published - timedelta(2)
                print("ATENÇÃO: Não houve publicação neste dia. Período de publicação do DOM-SP de terça a sábado. Data de solicitação ajustada para a última publicação.")
                break
            elif published.weekday() == 6:
                published = published - timedelta(1)
                print("ATENÇÃO: Não houve publicação neste dia. Período de publicação do DOM-SP de terça a sábado. Data de solicitação ajustada para a última publicação.")
                break
        elif published > datetime.now().date():
            published = houve_publicacao(datetime.now().date())
        else:
            published = published
            break
    return published

def foi_baixado(self):
    '''Método que verfica se os arquivos foram baixados, tratados e lista os arquivos'''
    try: return True, subprocess.os.listdir(self.dir.remoto)
    except: return False, []

def foi_tratado(self):
    '''Método para verificar se os arquivos foram tratados'''
    if self.baixado == True: return bool(reduce(lambda a,b: (str(a).startswith('pg_',0,3)) + (str(b).startswith('pg_',0,3)), self.arquivos_baixados))
    else: return False

def baixar(self):
    # Variável para verificar o tempo de execução
    start_time = time()
    subprocess.os.chdir(self.dir.querido_diario)
    try:
        [subprocess.os.remove(subprocess.os.path.join(self.dir.remoto,arquivo)) for arquivo in self.arquivos_baixados]
        subprocess.os.removedirs(self.dir.remoto)
        print("Arquivos apagados")
    except FileNotFoundError:
        print("Diretório não existe")
        pass 
    subprocess.os.chdir(self.dir.querido_diario)
    print("\n### BAIXANDO O DIÁRIO ###")
    if self.varacompanhar == True:
        input()
        pass
    subprocess.call(["scrapy","crawl","sp_sao_paulo","-a",f"start_date={str(self.published)}","-a",f"end_date={str(self.published)}"])
    print("Diário baixado")
    self.baixado, self.arquivos_baixados = foi_baixado(self)
    self.tratado = foi_tratado(self)
    self.year, self.edition, self.pags, self.head, self.dom = obter_informacao_dom(self)
    tratar_remoto(self)
    self.year, self.edition, self.pags, self.head, self.dom = obter_informacao_dom(self)
    remoto_merge_local(self)
    local_convert_tsv(self)
    local_limpa_dados(self)
    obter_informacao_dom(self)
    end_time = time()
    print(f'### TEMPO DE EXECUÇÃO: {timedelta(seconds=round(end_time - start_time,2))} ###')

def obter_informacao_dom(self):
        '''
        Obtém as informações do DOM.
                return YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM        
        '''
        try:
            DATA_DIR = self.dir.remoto
            DATA_FILES = subprocess.os.listdir(DATA_DIR)
            PAGS_DOM = str(len(DATA_FILES))
            with fz.open(subprocess.os.path.join(DATA_DIR,DATA_FILES[random.randint(0,int(PAGS_DOM)-1)])) as file:
                #print(file)
                contents = ''
                for page in file:
                        contents += page.get_text()
            HEAD_DOM = CABECALHO_DOM.search(contents).group(3)
            YEAR_DOM = CABECALHO_DOM.search(contents).group(4)
            EDITION_DOM = CABECALHO_DOM.search(contents).group(5)
            PAG_EVEN_DOM = CABECALHO_DOM.search(contents).group(2)
            PAG_ODD_DOM = CABECALHO_DOM.search(contents).group(7)
            PAG_DOM = (str(PAG_EVEN_DOM) + str(PAG_ODD_DOM)).replace('None','')

            PAGS_DOM = str(len(DATA_FILES))
            DOM = f'DOM_SP-{str(YEAR_DOM)}_{str(EDITION_DOM)}_{PAGS_DOM}_{str(self.published)}'

            print('\n### INFO: DOM-SP ###')
            print(f'DATA: {self.published}')
            print(f'YEAR: {YEAR_DOM}')
            print(f'EDIT: {EDITION_DOM}')
            print(f'PAGS: {PAGS_DOM}')
            print(f'HEAD: {HEAD_DOM}')
            print(f' DOM: {DOM}')
            return YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM,DOM
        except:
            YEAR_DOM = date.today().year - 1955
            HEAD_DOM ='São Paulo, Y (E)'
            PAGS_DOM = ''
            EDITION_DOM = ''
            DOM = ''
            print('\n### INFO: DOM-SP - DIÁRIO NÃO BAIXADO DESEJA BAIXAR? ###\n')
            #print('Pressione (S) para baixar ou pressione CTRL+C para cancelar')
            #tecla = input()
            #primeira_vez = True
            #print("varbaixar: ",self.varbaixar)
            #print("baixado: ",self.baixado)
            if self.varbaixar == True and self.baixado == False:
                self.pri = False
                baixar(self)
                self.baixado, self.arquivos_baixados = foi_baixado(self)
            return YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM,DOM

def tratar_remoto(self):
    '''
    Trata o diretório remoto renomeando os arquivos por página
    '''
    obter_informacao_dom(self)
    print("\n### RENOMEANDO OS ARQUIVOS ###")
    if self.varacompanhar == True:
        input()
        pass
    try:
        DATA_DIR = self.dir.remoto
        DATA_FILES = subprocess.os.listdir(DATA_DIR)
        for file_name in DATA_FILES:
            print('Rename de: ' + file_name)
            with fz.open(subprocess.os.path.join(DATA_DIR,file_name)) as file:
                context = ""
                for page in file:
                    context += '<pag>\n'+ page.get_text() + '</pag>\n'
                    print(CABECALHO_DOM.search(context))
                    if CABECALHO_DOM.search(context) != None:
                            PAG_EVEN_DOM = CABECALHO_DOM.search(context).group(2)
                            PAG_ODD_DOM = CABECALHO_DOM.search(context).group(7)
                            if  PAG_ODD_DOM != None:
                                    num_page = PAG_ODD_DOM
                            elif PAG_EVEN_DOM != None:
                                num_page = PAG_EVEN_DOM
                            elif CABECALHO_DOM.search(context).group() == self.head:
                                num_page = str(len(DATA_FILES))
                    elif context.find("Ano "+ str(self.year)) != -1:
                            num_page = '1'
                    else:
                            num_page = ''
            subprocess.os.rename(subprocess.os.path.join(DATA_DIR,file_name),subprocess.os.path.join(DATA_DIR,f'pg_{(num_page.strip()).zfill(3)}-{file_name}'))
        
        self.dir.arquivos_baixados = subprocess.os.listdir(DATA_DIR)
        self.dir.arquivos_baixados.sort()
        print(f'\n### RENAME CONCLUÍDO - Verifique a pasta: {DATA_DIR} ###')
    except IOError as erro:
        print(f'### RENAME: ERRO {erro}')

def remoto_merge_local(self):
    '''
    Junta todos os arquivos pdf
    '''
    print(f'\n### MERGE DOS ARQUIVOS PDF ###')
    if self.varacompanhar == True:
        input()
        pass
    DATA_FILES = [f for f in subprocess.os.listdir(self.dir.remoto) if f.endswith("pdf")]
    DATA_FILES.sort()
    merger = PdfFileMerger()
    #[merger.append(PdfFileReader(subprocess.os.path.join(self.dir.remoto, filename), "rb")) for filename in DATA_FILES]
    for filename in DATA_FILES:
        print(f'Merge de: {filename}')
        merger.append(PdfFileReader(subprocess.os.path.join(self.dir.remoto, filename), "rb"))
    merger.write(subprocess.os.path.join(self.dir.dom ,f"{self.dom}.pdf"))
    print(f'### MERGE CONCLUÍDO - Verifique a pasta: {self.dir.dom} ###')    

def local_convert_tsv(self):
    '''
    Converte o pdf em tsv
    '''
    print(f'\n### CONVERTENDO OS DADOS DO PDF PARA TXT ###')
    if self.varacompanhar == True:
        input()
        pass
    try:
        area_text = [[42.849,28.172,1209.134,215.329],[42.849,216.314,1210.119,393.621],[42.849,395.591,1210.119,574.868],[42.849,576.838,1207.164,760.055]]
        #tabula.convert_into_by_batch(SAVE_DIR,output_format="tsv",area=area_text,pages="all")
        convert_into_by_batch(self.dir.dom,output_format="tsv",area=area_text,pages="all")
        print(f'### CONVERT CONCLUÍDO - Verifique a pasta: {self.dir.dom} ###')
    except EOFError as erro:
        print(f'### CONVERT CONCLUÍDO COM EXCEÇÃO - Verifique a pasta: {self.dir.dom}\n{erro} ###')

def local_limpa_dados(self):
    '''
    Limpa os dados do conteúdo de quebra de linha, separador silábico, preposições, pronomes e conjunções 
    '''
    print(f'\n### LIMPANDO OS DADOS ARQUIVO TXT ###')
    if self.varacompanhar == True:
        input()
        pass
    try:
        #print('Limpando dados')
        DATA_FILES = [f for f in subprocess.os.listdir(self.dir.dom) if f.endswith("tsv")]
        DATA_FILES.sort()
        for filename in DATA_FILES:
            print(f'\n### LIMPANDO OS DADOS {filename} ###')
            with open(subprocess.os.path.join(self.dir.dom, filename), 'rb') as file:
                rawdata = file.read()
            encoding = chardet.detect(rawdata)['encoding']
            with open(subprocess.os.path.join(self.dir.dom, filename), 'r', encoding=encoding) as file:
                contents = file.read()
            contents = limpa_dados_preposicao_conjuncao(contents)
            contents = limpa_dados(contents)
            with open(subprocess.os.path.join(self.dir.dom, f"TRATADO_{filename}"), 'w', encoding='utf-8') as file:
                file.write(contents)
            contents = limpa_dados_servidores(self,contents)
        print(f'### LIMPEZA CONCLUÍDA - Verifique a pasta: {self.dir.dom} ###')
    except EOFError as erro:
        print(f'### LIMPEZA CONCLUÍDA COM EXCEÇÃO - Verifique a pasta: {self.dir.dom}\n{erro} ###')

