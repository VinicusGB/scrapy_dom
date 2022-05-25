from datetime import date, datetime, timedelta
from os import getcwd, path, listdir, chdir
from tabula import read_pdf, environment_info, convert_into_by_batch
from PyPDF2 import PdfFileReader, PdfFileMerger
import base
import os
import fitz as fz
import tabula

dt_now = base.get_date_today()


dt_now = date.today()
year_edition_dom = date.today().year - 1955
head_dom ='São Paulo, ' + str(year_edition_dom) + ' ('
if dt_now.weekday() == 0:
        dt_now = dt_now + timedelta(-2)
        dt_now = dt_now.strftime("%Y-%m-%d")
else:
        dt_now = dt_now.strftime("%Y-%m-%d")


BASE_DIR = os.getcwd()
os.chdir(BASE_DIR)
try:
    os.makedirs(f'{BASE_DIR}\\outputs_files\\{dt_now}')
    print(f'### MAKEDIRS CONCLUÍDO - Verifique a pasta: {BASE_DIR}\\outputs_files\\{dt_now}')
except:
    print(f'### MAKEDIRS PASTA EXISTENTE - Verifique a pasta: {BASE_DIR}\\outputs_files\\{dt_now}')
    pass


DIR_DATA = BASE_DIR + '\\querido-diario\\data_collection\\data\\3550308\\'+ str(dt_now)
SAVE_DIR = BASE_DIR + '\\outputs_files\\' + dt_now
os.chdir(DIR_DATA)
list_files_names = os.listdir(DIR_DATA)

print('BASE_DIR: ' + BASE_DIR)
print('DIR_DATA: ' + DIR_DATA)
print('SAVE_DIR: ' + SAVE_DIR)
print('Data de referência do DOM-SP: ' + dt_now)
print('Quantidade de páginas do DOM-SP: ' + str(len(list_files_names)))


print('Obtendo edição de: ' + list_files_names[3])
with fz.open(DIR_DATA +'\\'+ list_files_names[3]) as file:
        search_edition = ''
        for page in file:
                search_edition += page.get_text()

search_edition = search_edition[search_edition.find(head_dom):]
edition_dom = search_edition[search_edition.find('(')+1:search_edition.find(')')]
head_dom ='São Paulo, ' + str(year_edition_dom) + ' (' + edition_dom + ')'
print('Cabeçalho: ' + head_dom)


contexts = ''
for file_name in list_files_names:
        print('Obtendo conteúdo de: ' + file_name)
        with fz.open(DIR_DATA +'\\'+ file_name) as file:
                context = ""
                for page in file:
                        context += '<pag>\n'+ page.get_text() + '</pag>\n'
                
                odd_page = "São Paulo, " + str(year_edition_dom) + " (" + str(edition_dom) + ") – "
                even_page = " – São Paulo, " + str(year_edition_dom) + " (" + str(edition_dom) + ")"

                if  context.find(odd_page) != -1:
                        num_page = context[context.find(odd_page)+21:context.find('\n',context.find(odd_page))]
                elif context.find(even_page) != -1:
                        num_page = context[context.find('\n',context.find(even_page)-5)+1:context.find(even_page)]
                elif context.find("D.O.C.; " + head_dom) != -1:
                        num_page = str(len(list_files_names))
                elif context.find("Ano "+ str(year_edition_dom)) != -1:
                        num_page = '1'
                else:
                        num_page = ''

        contexts += context
        os.rename(file_name, "pg_" + num_page.zfill(3) + "-" + file_name)

list_files_names = os.listdir(DIR_DATA)
list_files_names.sort()
print(f'### RENAME CONCLUÍDO - Verifique a pasta: {DIR_DATA} ###')


pdf_files = [f for f in os.listdir(DIR_DATA) if f.endswith("pdf")]
merger = PdfFileMerger()

for filename in pdf_files:
    print(f'Merge de: {filename}')
    merger.append(PdfFileReader(os.path.join(DIR_DATA, filename), "rb"))

merger.write(SAVE_DIR + "\\DOM_SP-"+ str(year_edition_dom) + "_" + str(edition_dom) + "_" + str(len(list_files_names)) + "_" + str(dt_now)+".pdf")
print(f'### MERGE CONCLUÍDO - Verifique a pasta: {SAVE_DIR} ###')


print('Convertendo arquivo para TSV')
area_text = [[42.849,28.172,1209.134,215.329],[42.849,216.314,1210.119,393.621],[42.849,395.591,1210.119,574.868],[42.849,576.838,1207.164,760.055]]
tabula.convert_into_by_batch(SAVE_DIR,output_format="tsv",area=area_text,pages="all")
print(f'### CONVERT CONCLUÍDO - Verifique a pasta: {SAVE_DIR} ###')
