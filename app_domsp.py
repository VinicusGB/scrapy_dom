#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scripts.essentials import boas_vindas, menu_escolha, diario

#pesquisa = consulta_dom_sp("joão gabriel guimarães")

boas_vindas()

while True:
    menu_escolha()
    escolha = input('Digite uma opção:')
    if escolha == '0':
        break
    elif escolha == '1':
        break
    elif escolha == '2':
        diario()
