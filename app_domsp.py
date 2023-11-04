#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scripts.essentials import boas_vindas, menu_escolha, diario

#pesquisa = consulta_dom_sp("joão gabriel guimarães")

boas_vindas()


menu_escolha()
escolha = input('Digite uma opção:')
if escolha == '0':
    # Encerra o programa
    print('Encerrando o programa...')
    exit()
elif escolha == '1':
    print('Consulta por termo')
elif escolha == '2':
    diario = diario()
