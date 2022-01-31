
import fitz as fz

with fz.open("remocao.pdf") as pdf:
    conteudo = ""
    for pagina in pdf:
        conteudo += pagina.get_text()


#Localizando o início da tabela de dados
indice_dados = conteudo.find('REG.FUN.')


dados = conteudo[indice_dados:]

dados.replace('\n', ' ')
dados.replace(' - ', ' ')

col = 1
#linha = list()
position = 0
separadados = dados
linhas = "REG.FUN,NOME,DE,PARA"
while separadados.find('-') != -1:
    if col == 1:
        position = separadados.find('-')
        if position != -1 and separadados[position-1].isnumeric() and separadados[position+1].isnumeric():
                info = separadados[position-7:position+5]
                info = info.strip()
                linhas = linhas + info + ','
                print(f'{separadados[position-7:position]} - {separadados[position-1].isnumeric()} - { separadados[position+1].isnumeric()}')
                #linha.append(info)
                print(f'coluna 01: {info}')
                separadados = separadados[position+6:]
                #print(separadados)
                #break
                col +=1
        else:
            separadados = separadados.replace('-', ' ',1)
            continue
    elif col  == 2:
        position = separadados.find('-')
        if position != -1 and separadados[position-1].isnumeric():
                info = separadados[0:position-6]
                info = info.strip()
                info = info.replace('\n', ' ')
                linhas = linhas + info + ','
                #linha.append(info)
                print(f'coluna 02: {info}')
                separadados = separadados[position-6:]
                #print(separadados)
                #break
                col +=1
        else:
            separadados = separadados.replace('-', ' ',1)
            continue
    elif col  == 3:
        position = separadados.find('-')
        if position != -1 and separadados[position-1].isnumeric():
                info = separadados[position-6:position]
                info = info.strip()
                linhas = linhas + info + ','
                #linha.append(info)
                print(f'coluna 03: {info}')
                separadados = separadados[position+2:]
                #print(separadados)
                #break
                col +=1
        else:
            separadados = separadados.replace('-', ' ',1)
            continue
    elif col  == 4:
        position = separadados.find('-')
        if position != -1 and separadados[position-1].isnumeric():
                info = separadados[position-6:position]
                info = info.strip()
                linhas = linhas + info + '\n'
                #linha.append(info)
                print(f'coluna 04: {info}')
                separadados = separadados[position+1:]
                #print(separadados)
                #break
                col = 1
        else:
            separadados = separadados.replace('-', ' ',1)
            continue

arquivo = open("teste.csv", "a", encoding="utf-8")
arquivo.write(linhas)