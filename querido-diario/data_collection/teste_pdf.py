from datetime import date, datetime, timedelta
from os import getcwd, path, listdir, chdir
import datetime
import os

dt_now = date.today()
year_edition_dom = dt_now.year - 1955
head_dom ='São Paulo, ' + str(year_edition_dom) + ' ('
if dt_now.weekday() == 0:
        dt_now = dt_now + timedelta(-2)
        dt_now = dt_now.strftime("%Y-%m-%d")
else:
        dt_now = dt_now.strftime("%Y-%m-%d")


BASE_DIR = os.getcwd()
DIR_DATA = os.path.join(BASE_DIR,'data\\3550308\\'+ str(dt_now))
os.chdir(BASE_DIR)
list_files_names = os.listdir(DIR_DATA)
file_test = DIR_DATA +'\\'+ list_files_names[31]


import fitz as fz

with fz.open(file_test) as file:
        contexts = ''
        for page in file:
                contexts += page.get_text()

with open("..\\output_fitz.txt","w",encoding='utf-8-sig') as output_file:
    output_file.write(contexts)


import textract

context = ''
contexts = textract.process(file_test)
contexts = contexts.decode('utf-8-sig')

with open("..\\output_textract.txt","w",encoding='utf-8-sig') as output_file:
    output_file.write(contexts)


#pip install pypdf2
# importa as bibliotecas necessárias
import re
import PyPDF2

# Abre o arquivo pdf 
# lembre-se que para o windows você deve usar essa barra -> / 
# lembre-se também que você precisa colocar o caminho absoluto
pdf_file = open(file_test, 'rb')

#Faz a leitura usando a biblioteca
read_pdf = PyPDF2.PdfFileReader(pdf_file)

# pega o numero de páginas
number_of_pages = read_pdf.getNumPages()

#lê a primeira página completa
page = read_pdf.getPage(0)

#extrai apenas o texto
page_content = page.extractText()

# faz a junção das linhas 
parsed = ''.join(page_content)

with open("..\\output_pyPDF2.txt","w",encoding='utf-8-sig') as output_file:
    output_file.write(parsed)

print("Sem eliminar as quebras")
print(parsed)

# remove as quebras de linha
parsed = re.sub('n', '', parsed)
print("Após eliminar as quebras")
print(parsed)

print("nPegando apenas as 20 primeiras posições")
novastring = parsed[0:20]
print(novastring)

#Importando tabelas em pdf usando o pytabula
from tabula import read_pdf
# faz a leitura de uma tabela complexa
holerite = read_pdf(file_test)
# claramente o resultado mostra dataframe bastante mal formado. A ferramenta tem dificuldade de 
# compreender como a tabela é formada e transforma-la em algo manipulável.)
# faz a leitura de uma tabela comum
tabelaComum = read_pdf(file_test)
# bastante fácil de compreender e manipular os dados
#Exemplos: 
# retorna a primeira linha da tabela completa

with open("..\\output_tabula.txt","w",encoding='utf-8-sig') as output_file:
    output_file.write(holerite)

tabelaComum.iloc[0]
# pega o primeiro dado da tabela
tabelaComum.iloc[0][0]
# exibe todos os nomes da (primeira coluna)
#tabelaComum['Nome']
# exibe o primeiro nome da tabela 
#tabelaComum['Nome'][0]
#conta quantas linhas a tabela tem
#len(tabelaComum.iloc[0])


#pip install rows[pdf]
import rows

rows convert file_test arquivo.csv


'''
with open(file_test,'r',encoding='utf-8-sig') as file:
    contexts = ''
    for page in file.readlines():
            contexts += page.readline()

with open("..\\output_python.txt","w",encoding='utf-8-sig') as output_file:
    output_file.write(contexts)
'''
