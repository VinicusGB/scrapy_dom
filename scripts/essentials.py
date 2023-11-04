# -*- coding: utf-8 -*-

from core.domsp.classe import DOMSP
from datetime import date

def boas_vindas():
    print("\
#############################\n\
        SCRAPY DOM-SP\n\
#############################\n\
\n\
Bemvindo ao SCRAPY DOM-SP.\n\
Este projeto nasceu a partir do PROJETO de TCC da UNIVESP.\n\
E tem como objetivo WEB SCRAPY do Diário Oficial do Município de São Paulo (DOM-SP).\n\
Com a finalidade de facilitar o acesso, pesquisa e consulta do DOM-SP.\n\n\
=============================\n\
")

def menu_escolha():
    print("\
Escolha uma opção:\
\n\
1. Consulta geral a Imprensa Oficial\n\
2. Consulta ao Diário Oficial por dia\n\
0. Fechar o programa\
        ")

def diario():
    print('Digite a data de publicação para consulta')
    ano = input('Ano: ')
    mes = input('Mês: ')
    dia = input('Dia: ')
    dom_sp = DOMSP(date(int(ano),int(mes),int(dia)))
    return dom_sp
