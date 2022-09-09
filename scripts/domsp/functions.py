'''
Funções principais utilizadas na class domsp
'''

import subprocess
from pandas import read_csv, concat
from datetime import datetime, timedelta

def houve_publicacao(published):
    '''Obtém a data atual e retorna uma string: (YYYY-mm-dd)'''
    base = subprocess.os.getcwd()
    subprocess.os.chdir(base)
    feriadosmunicipais = read_csv(subprocess.os.path.join(base,'Feriados','docs','FeriadosMunicipaisBr.csv'),sep=';').query('UF == "SP" and NOME_DA_CIDADE == "São Paulo"')[['UF','NOME_DA_CIDADE','DIA','MÊS']]
    feriadosmunicipais['EVENTO'] = 'Aniversário do Município de São Paulo'
    feriadosestaduais = read_csv(subprocess.os.path.join(base,'Feriados','docs','FeriadosEstaduaisBr.csv'),sep=';').query('UF == "SP"')
    feriadosnacionais = read_csv(subprocess.os.path.join(base,'Feriados','docs','FeriadosNacionaisBr.csv'),sep=';')
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
