from datetime import date, datetime, timedelta
import os
import fitz as fz
import tabula

def get_date_today():
    '''Obtém a data atual e retorna uma string: (YYYY-mm-dd)'''
    dt_now = date.today()
    if dt_now.weekday() == 0:
            dt_now = dt_now + timedelta(-2)
            dt_now = dt_now.strftime("%Y-%m-%d")
    else:
            dt_now = dt_now.strftime("%Y-%m-%d")
    
    return dt_now

def get_directories():
        '''Obtém  os diretórios de trabalho.
                return BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES
        '''
        dt_now = get_date_today()
        BASE_DIR = os.getcwd()
        os.chdir(BASE_DIR)
        try:
                os.makedirs(f'{BASE_DIR}\\outputs_files\\{dt_now}')
        except:
                pass

        DATA_DIR = f'{BASE_DIR}\\querido-diario\\data_collection\\data\\3550308\\{str(dt_now)}'
        SAVE_DIR = f'{BASE_DIR}\\outputs_files\\{dt_now}'
        DATA_FILE = SAVE_DIR + '\\' + [f for f in os.listdir(SAVE_DIR) if f.endswith("tsv")][0]
        DATA_FILES = os.listdir(DATA_DIR)
        
        print(f'### INFO:  DIRS ###')
        print(f'BASE_DIR:  {BASE_DIR}')
        print(f'DATA_DIR:  {DATA_DIR}')
        print(f'SAVE_DIR:  {SAVE_DIR}')
        print(f'DATA_FILE  {DATA_FILE}')
        
        return BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES

def get_info_dom():
        '''Obtém as informações do DOM.
                return YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM        
        '''
        dt_now = get_date_today()
        BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES = get_directories()
        YEAR_DOM = date.today().year - 1955
        HEAD_DOM ='São Paulo, ' + str(YEAR_DOM) + ' ('

        with fz.open(DATA_DIR +'\\'+ DATA_FILES[3]) as file:
                search_edition = ''
                for page in file:
                        search_edition += page.get_text()

        search_edition = search_edition[search_edition.find(HEAD_DOM):]
        EDITION_DOM = search_edition[search_edition.find('(')+1:search_edition.find(')')]
        HEAD_DOM ='São Paulo, ' + str(YEAR_DOM) + ' (' + EDITION_DOM + ')'
        PAGS_DOM = str(len(DATA_FILES))

        print('### INFO: DOM-SP ###')
        print(f'DATA: {dt_now}')
        print(f'PAGS: {PAGS_DOM}')
        print(f'HEAD: {HEAD_DOM}')

        return YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM

def rename_pages_dom():
        '''Renomeia as páginas DOM.
                return DATA_FILES
        '''

        BASE_DIR,DATA_DIR,SAVE_DIR,DATA_FILE,DATA_FILES = get_directories()
        YEAR_DOM,EDITION_DOM,PAGS_DOM,HEAD_DOM = get_info_dom()

        print('### RENOMEANDO ARQUIVOS ###')

        contexts = ''
        for FILE_NAME in DATA_FILES:
                print('Obtendo conteúdo de: ' + FILE_NAME)
                with fz.open(f'{DATA_DIR}\\{FILE_NAME}') as FILE:
                        context = ""
                        for page in FILE:
                                context += '<pag>\n'+ page.get_text() + '</pag>\n'
                        
                        odd_page = "São Paulo, " + str(YEAR_DOM) + " (" + str(EDITION_DOM) + ") – "
                        even_page = " – São Paulo, " + str(YEAR_DOM) + " (" + str(EDITION_DOM) + ")"
                        
                        if  context.find(odd_page) != -1:
                                num_page = context[context.find(odd_page)+21:context.find('\n',context.find(odd_page))]
                        elif context.find(even_page) != -1:
                                num_page = context[context.find('\n',context.find(even_page)-5)+1:context.find(even_page)]
                        elif context.find("D.O.C.; " + HEAD_DOM) != -1:
                                num_page = str(len(DATA_FILES))
                        elif context.find("Ano "+ str(YEAR_DOM)) != -1:
                                num_page = '1'
                        else:
                                num_page = ''
                
                contexts += context
                os.rename(f'{DATA_DIR}\\{FILE_NAME}',f"{DATA_DIR}\\pg_{num_page.zfill(3)}-{FILE_NAME}")

        DATA_FILES = os.listdir(DATA_DIR)
        DATA_FILES.sort()

        os.chdir(BASE_DIR)

        print(f'### RENAME CONCLUÍDO - Verifique a pasta: {DATA_DIR} ###')

        return DATA_FILES


def save_csv(SAVE_DIR,CONTEXT,NAME_FILE):
        '''
                Cria um arquivo com o conteúdo e salva na pasta.
                        SAVE_DIR  : Diretório para salvar o conteúdo
                        CONTEXT   : Conteúdo a ser salvo
                        NAME_FILE : Nome do arquivo para ser salvo
        '''

        with open(f"{SAVE_DIR}\\{NAME_FILE}.txt","w",encoding='utf-8') as output_file:
                output_file.write(CONTEXT)
        
        return f"{SAVE_DIR}\\{NAME_FILE}.txt"

